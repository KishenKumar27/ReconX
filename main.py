from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from together import Together
import uuid
import uvicorn
import mysql.connector
from mysql.connector import Error
import os
import requests
from datetime import datetime, timedelta
import asyncio
from dotenv import load_dotenv
# from apscheduler.schedulers.background import BackgroundScheduler

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

class ReconcileData(BaseModel):
    reconciliation_id: str
    transaction_id: str
    discrepancy_category: str
    transaction_date: datetime
    payment_reference: str
    amount: float
    status: str
    gateway_status: str
    discrepancy_amount: float
    root_cause: str
    assigned_to: str
    resolution_status: str

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

def generate_llm_analysis(transaction: dict, payment_log: Optional[dict]) -> dict:
    prompt = f"""
    Analyze the given transaction data to identify the root cause of a potential financial discrepancy. Consider the transaction status, amount, currency, and gateway code, as well as any available payment log information.

    Key Data Points:
    - Transaction amount and currency: {transaction['amount']} {transaction['currency']}
    - Transaction status: {transaction['transaction_status']}
    - Payment log status: {payment_log.get('gateway_status', 'No log') if payment_log else 'Not available'}

    Search Results:
    {search_internet(f"{transaction['transaction_status']} {transaction['amount']} {transaction['currency']} discrepancy")}

    Provide a concise analysis in the following format:
    The root cause of the discrepancy is likely [root cause], based on [key evidence]. Confidence level: [High/Medium/Low]. 
    Then, provide 1-2 critical next steps as recommendations in a short paragraph.
    """

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": "You are a payment forensic analyst. Use systematic multi-step reasoning. Consider multiple angles before concluding."},
                {"role": "user", "content": prompt}
            ]
        )
        analysis = response.choices[0].message.content
        parts = analysis.split("\n\n")
        analysis_text = parts[0]
        recommendation_text = parts[1].strip()
        if recommendation_text.startswith("Recommendation:") or recommendation_text.startswith("Next steps:"):
            recommendation_text = recommendation_text.split(":")[1].strip()
        return {
            "analysis": analysis_text,
            "recommendation": recommendation_text
        }
    except Exception as e:
        return {
            "analysis": "Analysis error: unable to determine root cause",
            "recommendation": "Contact the payment gateway support team for further assistance.",
            "error": str(e)
        }



def get_duplicate_payments(transaction_id: str) -> List[dict]:
    # Check for duplicate payments in the payment log
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    query = """
        SELECT * FROM payment_logs WHERE transaction_id = %s
    """
    cursor.execute(query, (transaction_id,))
    payment_logs = cursor.fetchall()
    cursor.close()
    connection.close()
    return payment_logs if len(payment_logs) > 1 else []

def get_duplicate_transactions(transaction_id: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
        SELECT * FROM transactions
        WHERE payment_reference = (
            SELECT payment_reference FROM transactions
            WHERE transaction_id = %s
        ) AND transaction_id != %s
    """
    cursor.execute(query, (transaction_id, transaction_id))
    duplicate_transactions = cursor.fetchall()
    
    if duplicate_transactions:
        return [
            {
                "transaction_id": transaction[0],
                "amount": transaction[5],
                "status": transaction[7]
            } for transaction in duplicate_transactions
        ]
    else:
        return None

# @app.get("/detect_discrepancy")
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
    elif transaction['transaction_status'] != payment_log['gateway_status']:
        discrepancy_category = "Status Mismatch"
        is_discrepancy = True

    # Check for duplicate payments in the payment log
    duplicate_payments = get_duplicate_payments(transaction_id)
    if duplicate_payments and len(duplicate_payments) > 1:
        discrepancy_category = "Duplicate Payment"
        is_discrepancy = True
    
    root_cause = generate_llm_analysis(transaction, payment_log) if is_discrepancy else "No discrepancy detected"
    
    return {
        "transaction_id": transaction_id,
        "is_discrepancy": is_discrepancy,
        "discrepancy_category": discrepancy_category,
        "root_cause": root_cause
    }

# @app.get("/reconcile")
def reconcile(transaction_id: str):
    connection = get_db_connection()
    cursor = connection.cursor()
    
    transaction = get_transaction_by_id(transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    try:
        current_balance_query = f"SELECT COALESCE(SUM(amount), 0) FROM transactions WHERE transaction_status = 'Success' AND transaction_id = '{transaction_id}'"
        cursor.execute(current_balance_query)
        current_balance = cursor.fetchone()[0]
        
        reconciled_balance_query = f"""
            SELECT COALESCE(SUM(t.amount), 0) FROM transactions t
            JOIN payment_logs p ON t.transaction_id = p.transaction_id
            WHERE t.transaction_status = 'Success' AND p.gateway_status = 'Success' AND t.amount = p.gateway_amount AND transaction_id = '{transaction_id}'
        """
        cursor.execute(reconciled_balance_query)
        reconciled_balance = cursor.fetchone()[0]
        connection.commit()
        
        return {
            "current_balance": float(current_balance),
            "reconciled_balance": float(reconciled_balance),
        }
    except Exception as e:
        connection.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing reconciliation: {str(e)}")
    finally:
        cursor.close()
        connection.close()

# # Get all reconcile data
# def get_reconcile_data(
#     reconciliation_id: Optional[str] = None,
#     transaction_id: Optional[str] = None,
#     discrepancy_category: Optional[str] = None,
#     transaction_date: Optional[datetime] = None,
#     payment_reference: Optional[str] = None,
#     amount: Optional[float] = None,
#     status: Optional[str] = None,
#     gateway_status: Optional[str] = None,
#     discrepancy_amount: Optional[float] = None,
#     root_cause: Optional[str] = None,
#     assigned_to: Optional[str] = None,
#     resolution_status: Optional[str] = None
# ) -> List[dict]:
#     connection = get_db_connection()
#     cursor = connection.cursor(dictionary=True)
#     query = """
#         SELECT * FROM reconciliation_records
#         WHERE resolution_status != 'No Discrepancy' AND
#             (%s IS NULL OR reconciliation_id = %s) AND
#             (%s IS NULL OR transaction_id = %s) AND
#             (%s IS NULL OR discrepancy_category = %s) AND
#             (%s IS NULL OR transaction_date = %s) AND
#             (%s IS NULL OR payment_reference = %s) AND
#             (%s IS NULL OR amount = %s) AND
#             (%s IS NULL OR status = %s) AND
#             (%s IS NULL OR gateway_status = %s) AND
#             (%s IS NULL OR discrepancy_amount = %s) AND
#             (%s IS NULL OR root_cause = %s) AND
#             (%s IS NULL OR assigned_to = %s) AND
#             (%s IS NULL OR resolution_status = %s)
#     """
#     cursor.execute(query, (
#         reconciliation_id, reconciliation_id,
#         transaction_id, transaction_id,
#         discrepancy_category, discrepancy_category,
#         transaction_date, transaction_date,
#         payment_reference, payment_reference,
#         amount, amount,
#         status, status,
#         gateway_status, gateway_status,
#         discrepancy_amount, discrepancy_amount,
#         root_cause, root_cause,
#         assigned_to, assigned_to,
#         resolution_status, resolution_status
#     ))
#     reconcile_data = cursor.fetchall()
#     for data in reconcile_data:
#         if data['transaction_date']:
#             data['transaction_date'] = data['transaction_date'].strftime('%Y-%m-%d %H:%M:%S')
#     cursor.close()
#     connection.close()
#     return reconcile_data

def get_reconcile_data(
    reconciliation_id: Optional[str] = None,
    transaction_id: Optional[str] = None,
    transaction_date: Optional[datetime] = None,
    payment_reference: Optional[str] = None,
    amount: Optional[float] = None,
    status: Optional[str] = None,
    gateway_status: Optional[str] = None,
    discrepancy_amount: Optional[float] = None,
    root_cause: Optional[str] = None,
    assigned_to: Optional[str] = None,
    resolution_status: Optional[str] = None
) -> List[dict]:
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    discrepancy_categories = ['Missing Payments', 'Amount Mismatch', 'Status Mismatch', 'Duplicates']

    query_parts = []
    query_params = []

    for category in discrepancy_categories:
        query_parts.append("""
            (SELECT * FROM reconciliation_records
            WHERE discrepancy_category = %s
                AND (%s IS NULL OR reconciliation_id = %s)
                AND (%s IS NULL OR transaction_id = %s)
                AND (%s IS NULL OR transaction_date = %s)
                AND (%s IS NULL OR payment_reference = %s)
                AND (%s IS NULL OR amount = %s)
                AND (%s IS NULL OR status = %s)
                AND (%s IS NULL OR gateway_status = %s)
                AND (%s IS NULL OR discrepancy_amount = %s)
                AND (%s IS NULL OR root_cause = %s)
                AND (%s IS NULL OR assigned_to = %s)
                AND (%s IS NULL OR resolution_status = %s)
            ORDER BY transaction_date DESC
            LIMIT 2)
        """)
        query_params.extend([
            category,
            reconciliation_id, reconciliation_id,
            transaction_id, transaction_id,
            transaction_date, transaction_date,
            payment_reference, payment_reference,
            amount, amount,
            status, status,
            gateway_status, gateway_status,
            discrepancy_amount, discrepancy_amount,
            root_cause, root_cause,
            assigned_to, assigned_to,
            resolution_status, resolution_status
        ])

    final_query = " UNION ALL ".join(query_parts)

    cursor.execute(final_query, query_params)
    reconcile_data = cursor.fetchall()

    for data in reconcile_data:
        if data['transaction_date']:
            data['transaction_date'] = data['transaction_date'].strftime('%Y-%m-%d %H:%M:%S')

    cursor.close()
    connection.close()
    return reconcile_data

async def check_and_update_discrepancies():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    # Check for unscanned transactions
    query = """
        SELECT * FROM transactions
        WHERE transaction_id NOT IN (SELECT transaction_id FROM reconciliation_records)
    """
    cursor.execute(query)
    unscanned_transactions = cursor.fetchall()
    
    for transaction in unscanned_transactions:
        transaction["transaction_status"]

        # Perform discrepancy detection and reconciliation
        discrepancy_result = detect_discrepancy(transaction['transaction_id'])

        # Get gateway status from payment logs
        gateway_status_query = """
            SELECT * FROM payment_logs
            WHERE transaction_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """
        cursor.execute(gateway_status_query, (transaction['transaction_id'],))
        gateway_status_result = cursor.fetchone()
        gateway_status = gateway_status_result.get('gateway_status') if gateway_status_result else None

        if gateway_status_result is None:
            gateway_amount = None
        else:
            gateway_amount = float(gateway_status_result.get('gateway_amount', None))

        if gateway_amount is None:
            discrepancy_amount = -1
        else:
            discrepancy_amount = abs(float(transaction.get('amount')) - float(gateway_status_result.get('gateway_amount')))

        # Set reconciled_balance to gateway_amount if available
        reconciled_balance = gateway_amount if gateway_amount is not None else None

        # Determine resolution status based on new conditions
        if gateway_status == "Success" and transaction.get('transaction_status') == "Success":
            if discrepancy_amount == 0:
                resolution_status = 'No Discrepancy'
            else:
                resolution_status = 'Resolved'
        else:
            resolution_status = 'Unresolved'

        if resolution_status == "Unresolved" or resolution_status == "No Discrepancy":
            reconciled_balance = None

        if discrepancy_result['is_discrepancy']:
            try:
                insert_query = """
                    INSERT INTO reconciliation_records (
                        reconciliation_id,
                        transaction_id,
                        discrepancy_category,
                        transaction_date,
                        payment_reference,
                        amount,
                        status,
                        gateway_status,
                        discrepancy_amount,
                        root_cause,
                        assigned_to,
                        resolution_status,
                        balance,
                        reconciled_balance
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """

                cursor.execute(insert_query, (
                    str(uuid.uuid4()),
                    transaction.get('transaction_id'), 
                    discrepancy_result.get('discrepancy_category', ''),  
                    transaction.get('transaction_date'),  
                    transaction.get('payment_reference', ''),  
                    transaction.get('amount'),  
                    transaction.get('transaction_status'),  
                    gateway_status,  
                    discrepancy_amount,  
                    discrepancy_result.get('root_cause', '').get('analysis', ''),  
                    None,  
                    resolution_status,
                    transaction.get('amount'),  
                    reconciled_balance  
                ))

                connection.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")
        else:
            try:
                insert_query = """
                    INSERT INTO reconciliation_records (
                        reconciliation_id,
                        transaction_id,
                        transaction_date,
                        payment_reference,
                        amount,
                        status,
                        gateway_status,
                        assigned_to,
                        resolution_status,
                        balance,
                        reconciled_balance
                    )
                    VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                """

                cursor.execute(insert_query, (
                    str(uuid.uuid4()),
                    transaction.get('transaction_id'),
                    transaction.get('transaction_date'),
                    transaction.get('payment_reference', ''),
                    transaction.get('amount'),
                    transaction.get('transaction_status'),
                    gateway_status,
                    None,
                    resolution_status,
                    transaction.get('amount'),
                    reconciled_balance
                ))

                connection.commit()
            except Exception as e:
                print(f"Error inserting data: {e}")
        print("Data Inserted")
    
    # Check for unresolved reconciliations
    query = """
        SELECT r.*, t.* FROM reconciliation_records r
        JOIN transactions t ON r.transaction_id = t.transaction_id
        WHERE r.resolution_status = 'Unresolved'
    """
    cursor.execute(query)
    unresolved_reconciliations = cursor.fetchall()
    
    for reconciliation in unresolved_reconciliations:
        # Get gateway status from payment logs
        gateway_status_query = """
            SELECT * FROM payment_logs
            WHERE transaction_id = %s
            ORDER BY timestamp DESC
            LIMIT 1
        """
        cursor.execute(gateway_status_query, (reconciliation['transaction_id'],))
        gateway_status_result = cursor.fetchone()
        gateway_status = gateway_status_result.get('gateway_status') if gateway_status_result else None

        if gateway_status_result is None:
            gateway_amount = None
        else:
            gateway_amount = float(gateway_status_result.get('gateway_amount', None))

        if gateway_amount is None or gateway_status_result != "Success":
            discrepancy_amount = -1
        else:
            discrepancy_amount = abs(float(reconciliation.get('amount')) - gateway_amount)

        # Set reconciled_balance to gateway_amount if available
        reconciled_balance = gateway_amount if gateway_amount is not None else None

        # Determine resolution status based on new conditions
        if gateway_status == "Success" and reconciliation.get('transaction_status') == "Success":
            if discrepancy_amount == 0:
                resolution_status = 'No Discrepancy'
            else:
                resolution_status = 'Resolved'
        else:
            resolution_status = 'Unresolved'

        if discrepancy_result['is_discrepancy']:
            update_query = """
                UPDATE reconciliation_records
                SET 
                    discrepancy_category = %s,
                    status = %s,
                    gateway_status = %s,
                    discrepancy_amount = %s,
                    root_cause = %s,
                    resolution_status = %s,
                    balance = %s,
                    reconciled_balance = %s
                WHERE reconciliation_id = %s
            """
            cursor.execute(update_query, (
                discrepancy_result.get('discrepancy_category', ''),
                reconciliation.get('transaction_status'),
                gateway_status,
                discrepancy_amount,
                discrepancy_result.get('root_cause', '').get('analysis', ''),
                resolution_status,
                reconciliation.get('amount'),
                reconciled_balance,
                reconciliation['reconciliation_id']
            ))
            connection.commit()
        else:
            update_query = """
                UPDATE reconciliation_records
                SET 
                    discrepancy_category = NULL,
                    status = %s,
                    gateway_status = %s,
                    discrepancy_amount = %s,
                    root_cause = NULL,
                    resolution_status = %s,
                    balance = %s,
                    reconciled_balance = %s
                WHERE reconciliation_id = %s
            """
            cursor.execute(update_query, (
                reconciliation.get('transaction_status'),
                gateway_status,
                discrepancy_amount,
                resolution_status,
                reconciliation.get('amount'),
                reconciled_balance,
                reconciliation['reconciliation_id']
            ))
            connection.commit()
    
    cursor.close()
    connection.close()


@app.get("/reconcile_data")
def get_reconcile_data_api(
    reconciliation_id: Optional[str] = Query(None),
    transaction_id: Optional[str] = Query(None),
    discrepancy_category: Optional[str] = Query(None),
    transaction_date: Optional[datetime] = Query(None),
    payment_reference: Optional[str] = Query(None),
    amount: Optional[float] = Query(None),
    status: Optional[str] = Query(None),
    gateway_status: Optional[str] = Query(None),
    discrepancy_amount: Optional[float] = Query(None),
    root_cause: Optional[str] = Query(None),
    assigned_to: Optional[str] = Query(None),
    resolution_status: Optional[str] = Query(None)
):
    # return get_reconcile_data(
    #     reconciliation_id,
    #     transaction_id,
    #     discrepancy_category,
    #     transaction_date,
    #     payment_reference,
    #     amount,
    #     status,
    #     gateway_status,
    #     discrepancy_amount,
    #     root_cause,
    #     assigned_to,
    #     resolution_status
    # )

    return get_reconcile_data(
        reconciliation_id,
        transaction_id,
        transaction_date,
        payment_reference,
        amount,
        status,
        gateway_status,
        discrepancy_amount,
        root_cause,
        assigned_to,
        resolution_status
    )

@app.get("/transaction_stats")
def get_transaction_stats():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        # Count all scanned transactions
        scanned_query = """
            SELECT COUNT(*) as count
            FROM reconciliation_records r
            JOIN transactions t ON r.transaction_id = t.transaction_id
        """
        cursor.execute(scanned_query)
        scanned_count = cursor.fetchone()['count']
        
        # Count unresolved transactions
        unresolved_query = """
            SELECT COUNT(*) as count
            FROM reconciliation_records r
            JOIN transactions t ON r.transaction_id = t.transaction_id
            WHERE r.resolution_status = 'Unresolved'
        """
        cursor.execute(unresolved_query)
        unresolved_count = cursor.fetchone()['count']
        
        # Count resolved transactions
        resolved_query = """
            SELECT COUNT(*) as count
            FROM reconciliation_records r
            JOIN transactions t ON r.transaction_id = t.transaction_id
            WHERE r.resolution_status IN ('Resolved')
        """
        cursor.execute(resolved_query)
        resolved_count = cursor.fetchone()['count']
        
        return {
            "scanned_transactions": scanned_count,
            "unresolved_transactions": unresolved_count,
            "resolved_transactions": resolved_count,
            "resolution_rate": round(resolved_count / (unresolved_count + resolved_count) * 100, 2) if scanned_count > 0 else 0
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching transaction statistics: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/discrepancy_categories")
def get_discrepancy_categories():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        query = """
            SELECT discrepancy_category, COUNT(*) as count
            FROM reconciliation_records
            GROUP BY discrepancy_category
        """
        cursor.execute(query)
        categories = cursor.fetchall()
        
        category_mapping = {
            "Missing Payments": 0,
            "Amount Mismatch": 0,
            "Status Mismatch": 0,
            "Duplicates": 0,
            "No Discrepancy": 0
        }
        
        for category in categories:
            if category['discrepancy_category'] in category_mapping:
                category_mapping[category['discrepancy_category']] = category['count']
            elif category['discrepancy_category'] is None:
                category_mapping["No Discrepancy"] = category['count']
        
        result = {
            "xaxis": {
                "categories": list(category_mapping.keys())
            },
            "series": [
                {
                    "data": list(category_mapping.values())
                }
            ]
        }
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching discrepancy categories: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.get("/discrepancy_cases")
def get_discrepancy_cases():
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    try:
        today = datetime.now().date()
        this_week_start = (datetime.now() - timedelta(days=datetime.now().weekday())).date()
        this_month_start = datetime(datetime.now().year, datetime.now().month, 1).date()

        query = """
            SELECT 
                SUM(CASE WHEN transaction_date = %s THEN 1 ELSE 0 END) as today,
                SUM(CASE WHEN transaction_date >= %s THEN 1 ELSE 0 END) as this_week,
                SUM(CASE WHEN transaction_date >= %s THEN 1 ELSE 0 END) as this_month
            FROM reconciliation_records
            WHERE discrepancy_category IS NOT NULL AND discrepancy_category != 'No Discrepancy'
        """
        cursor.execute(query, (today, this_week_start, this_month_start))
        result = cursor.fetchone()

        return [
            {"id": 1, "type": "Today", "total": f"{result['today']:,}"},
            {"id": 2, "type": "This Week", "total": f"{result['this_week']:,}"},
            {"id": 3, "type": "This Month", "total": f"{result['this_month']:,}"}
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching discrepancy cases: {str(e)}")

    finally:
        cursor.close()
        connection.close()


async def run_schedule():
    while True:
        await check_and_update_discrepancies()
        await asyncio.sleep(3600)  # Run every hour

# Run the scheduler as an asynchronous task
async def main():
    task = asyncio.create_task(run_schedule())
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, lambda: uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=False, workers=1))

if __name__ == "__main__":
    asyncio.run(main())