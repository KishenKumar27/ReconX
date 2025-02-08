from fastapi import FastAPI, Query, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from together import Together
import uuid
import uvicorn
import mysql.connector
from mysql.connector import Error
import os
import requests
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# MySQL Database configuration
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")
DB_HOST = os.getenv("DB_HOST", "127.0.0.1")
DB_PORT = os.getenv("DB_PORT", "3307")
DB_NAME = os.getenv("DB_NAME", "trading_platform")

# SerpAPI configuration
SERPER_API_KEY = os.getenv("SERPER_API_KEY")

# Database connection function
def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
            port=DB_PORT
        )
        if connection.is_connected():
            return connection
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database connection error: {str(e)}")

# Pydantic models
class Transaction(BaseModel):
    transaction_id: str
    amount: float
    currency: str
    transaction_status: str
    transaction_date: datetime
    payment_method: str
    processing_fee: float
    net_amount: float

class PaymentLog(BaseModel):
    log_id: str
    transaction_id: str
    gateway_amount: float
    gateway_currency: str
    gateway_status: str
    timestamp: datetime

class ReconcileRequest(BaseModel):
    discrepancy_category: str
    possible_root_cause: str
    transaction_id: str

def get_transaction_by_id(transaction_id: str) -> Optional[dict]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT * FROM transactions WHERE transaction_id = %s
    """
    cursor.execute(query, (transaction_id,))
    transaction = cursor.fetchone()
    cursor.close()
    connection.close()
    return transaction

def get_payment_log_by_transaction_id(transaction_id: str) -> Optional[dict]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT * FROM payment_logs WHERE transaction_id = %s ORDER BY timestamp DESC LIMIT 1
    """
    cursor.execute(query, (transaction_id,))
    payment_log = cursor.fetchone()
    cursor.close()
    connection.close()
    return payment_log

# Function to perform an internet search using Serper API
def search_internet(query: str) -> str:
    url = "https://google.serper.dev/search"
    headers = {"X-API-KEY": SERPER_API_KEY}
    params = {"q": query, "location": "United States"}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'organic' in data:
            return "\n".join([result['snippet'] for result in data['organic']])
    return "No results found."

def generate_llm_analysis(transaction: dict, payment_log: Optional[dict]) -> str:
    prompt = f"""
    Transaction Details: 
    - Amount: {transaction['amount']}
    - Status: {transaction['transaction_status']}
    - Currency: {transaction['currency']}
    
    Payment Log Details: {payment_log if payment_log else 'No payment log found'}
    
    Analyze the discrepancy and provide the most likely root cause.
    """
    
    # Perform an internet search for additional context
    search_query = f"Financial discrepancy {transaction['transaction_status']} {transaction['currency']} {transaction['amount']}"
    search_results = search_internet(search_query)
    
    prompt += f"\n\nInternet Search Results:\n{search_results}"
    
    try:
        response = client.chat.completions.create(
            model="meta-llama/Llama-3.3-70B-Instruct-Turbo",
            messages=[
                {"role": "system", "content": "You are a financial reconciliation expert."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error generating analysis: {str(e)}"

@app.get("/detect_discrepancy")
def detect_discrepancy(transaction_id: str = Query(..., description="Transaction ID to check")):
    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    payment_log = get_payment_log_by_transaction_id(transaction_id)
    discrepancy_category = None
    is_discrepancy = False
    
    if not payment_log:
        discrepancy_category = "Missing Payments"
        is_discrepancy = True
    elif float(transaction['amount']) != float(payment_log['gateway_amount']):
        discrepancy_category = "Amount Mismatch"
        is_discrepancy = True
    elif transaction['transaction_status'] == "Pending" and payment_log['gateway_status'] == "Success":
        discrepancy_category = "Status Mismatch"
        is_discrepancy = True
    
    possible_root_cause = generate_llm_analysis(transaction, payment_log) if is_discrepancy else "No discrepancy detected"
    
    return {
        "transaction_id": transaction_id,
        "is_discrepancy": is_discrepancy,
        "discrepancy_category": discrepancy_category,
        "possible_root_cause": possible_root_cause
    }

@app.post("/reconcile")
def reconcile(request: ReconcileRequest):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    transaction = get_transaction_by_id(request.transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    try:
        current_balance_query = "SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_status = 'Completed'"
        cursor.execute(current_balance_query)
        current_balance = cursor.fetchone()[0]
        
        reconciled_balance_query = """
            SELECT COALESCE(SUM(t.amount), 0) FROM transactions t
            JOIN payment_logs p ON t.transaction_id = p.transaction_id
            WHERE t.transaction_status = 'Completed' AND p.gateway_status = 'Success'
        """
        cursor.execute(reconciled_balance_query)
        reconciled_balance = cursor.fetchone()[0]
        
        audit_query = """
            INSERT INTO audit_logs (audit_id, transaction_id, action, performed_by, timestamp)
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(audit_query, (
            str(uuid.uuid4()), request.transaction_id,
            f"Manual reconciliation: {request.discrepancy_category}", "system", datetime.now()
        ))
        connection.commit()
        
        return {
            "current_balance": float(current_balance),
            "reconciled_balance": float(reconciled_balance),
            "discrepancy_category": request.discrepancy_category,
            "possible_root_cause": request.possible_root_cause
        }
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing reconciliation: {str(e)}")
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    uvicorn.run("new_main:app", host="0.0.0.0", port=8000, reload=False, workers=1)