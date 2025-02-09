from fastapi import FastAPI, Query, HTTPException, UploadFile, File
import traceback
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from together import Together
import uuid
import uvicorn
import mysql.connector
from mysql.connector import Error
import os
import requests
from datetime import datetime, timedelta
import asyncio
import json
from decimal import Decimal
from dotenv import load_dotenv
import pandas as pd
import io
import tiktoken
from functools import partial
import aiomysql
# from apscheduler.schedulers.background import BackgroundScheduler

load_dotenv()

app = FastAPI()
client = Together(api_key=os.getenv("TOGETHER_API_KEY"))

# MySQL Database configuration
DB_USER = os.getenv("DB_USER", "app_user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "app_password")
DB_HOST = os.getenv("DB_HOST", "10.10.240.93")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "payment_resolution")

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

async def create_reconciliation_summaries_table():
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS reconciliation_summaries (
                summary_id VARCHAR(255) PRIMARY KEY,
                timestamp DATETIME,
                total_transactions INT,
                discrepancy_count INT,
                resolution_rate FLOAT
                -- Add other fields as needed
            )
        """)
        connection.commit()
        print("reconciliation_summaries table created or already exists.")
    except Error as e:
        print(f"Error creating reconciliation_summaries table: {e}")
        connection.rollback()
        raise  # Re-raise the exception to potentially stop startup
    finally:
        cursor.close()
        connection.close()

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

async def async_get_transaction_by_id(cursor, connection, transaction_id: str) -> Optional[dict]:
    query = """
        SELECT * FROM transactions WHERE transaction_id = %s
    """

    await cursor.execute(query, (transaction_id,))
    transaction = await cursor.fetchone()

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

def count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """Count the number of tokens in a text string."""
    try:
        encoding = tiktoken.encoding_for_model(model)
        return len(encoding.encode(text))
    except KeyError:
        # Fallback to cl100k_base encoding if model not found
        encoding = tiktoken.get_encoding("cl100k_base")
        return len(encoding.encode(text))

def generate_llm_analysis(transaction: tuple, payment_log: Optional[tuple]) -> dict:
    try:
        gateway_status = payment_log[4]
    except:
        gateway_status = "Not available"

    # Construct the prompt
    prompt = f"""
    Analyze the given transaction data to identify the root cause of a potential financial discrepancy. Consider the transaction status, amount, currency, and gateway code, as well as any available payment log information.
    Key Data Points:
    - Transaction amount and currency: {transaction[5]} {transaction[6]}
    - Transaction status: {transaction[7]}
    - Payment log status: {gateway_status}
    Search Results:
    {search_internet(f"{transaction[7]} {transaction[5]} {transaction[6]} discrepancy")}
    Provide a concise analysis in the following format:
    The root cause of the discrepancy is likely [root cause], based on [key evidence]. Confidence level: [High/Medium/Low].
    Then, provide 1-2 critical next steps as recommendations in a short paragraph.
    """

    # Initialize token counters
    token_counts = {
        "system_prompt": count_tokens("You are a payment forensic analyst. Use systematic multi-step reasoning. Consider multiple angles before concluding."),
        "user_prompt": count_tokens(prompt),
        "total_input": 0,
        "response": 0
    }
    
    token_counts["total_input"] = token_counts["system_prompt"] + token_counts["user_prompt"]

    try:
        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": "You are a payment forensic analyst. Use systematic multi-step reasoning. Consider multiple angles before concluding."},
                {"role": "user", "content": prompt}
            ]
        )
        
        analysis = response.choices[0].message.content
        token_counts["response"] = count_tokens(analysis)
        
        # Print token usage information
        print("\nToken Usage Breakdown:")
        print(f"System Prompt: {token_counts['system_prompt']} tokens")
        print(f"User Prompt: {token_counts['user_prompt']} tokens")
        print(f"Response: {token_counts['response']} tokens")
        print(f"Total Input: {token_counts['total_input']} tokens")
        print(f"Total Tokens: {token_counts['total_input'] + token_counts['response']} tokens")
        
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
        print("\nToken Usage (Error Case):")
        print(f"Input Tokens: {token_counts['total_input']}")
        error_message = "Analysis error: unable to determine root cause"
        print(f"Error Message Tokens: {count_tokens(error_message)}")
        
        return {
            "analysis": error_message,
            "recommendation": "Contact the payment gateway support team for further assistance.",
            "error": str(e)
        }

def datetime_handler(obj):  # Custom JSON serializer
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO string
    raise TypeError("Object of type {} is not JSON serializable".format(type(obj)))


def custom_serializer(obj):  # Combined custom serializer
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO string
    if isinstance(obj, Decimal):
        return str(obj)  # Convert Decimal to string
    raise TypeError(f"Object of type {type(obj)} is not JSON serializable")


async def async_count_tokens(text: str, model: str = "gpt-3.5-turbo") -> int:
    """
    Asynchronously count the number of tokens in a text string.
    Uses an executor to avoid blocking on CPU-intensive tokenization.
    """
    def _count_tokens(text: str, model: str) -> int:
        try:
            encoding = tiktoken.encoding_for_model(model)
            return len(encoding.encode(text))
        except KeyError:
            encoding = tiktoken.get_encoding("cl100k_base")
            return len(encoding.encode(text))
    
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, partial(_count_tokens, text, model))

def generate_llm_summary(reconciliation_records: List[dict]) -> str:
    if not reconciliation_records:
        print("Token usage: 0 (no records to process)")
        return "No reconciliation records found."

    # Initialize token counters
    token_counts = {
        "system_prompt": count_tokens("You are a payment forensic analyst summarizing reconciliation data."),
        "records_tokens": 0,
        "prompt_template_tokens": 0,
        "total_input": 0,
        "response": 0
    }

    try:
        # Serialize records
        serializable_records = []
        for record in reconciliation_records:
            serializable_record = {}
            for key, value in record.items():
                if isinstance(value, (datetime, Decimal)):
                    serializable_record[key] = custom_serializer(value)
                else:
                    serializable_record[key] = value
            serializable_records.append(serializable_record)

        records_string = json.dumps(serializable_records, default=custom_serializer)
        token_counts["records_tokens"] = count_tokens(records_string)

        prompt = f"""
        You are a payment forensic analyst. Analyze the following reconciliation records and summarize the key root causes of discrepancies in a clear and concise paragraph. 
        Focus on identifying common patterns, trends, and their frequency (e.g., "Amount mismatches caused 60% of discrepancies"). Keep the summary brief yet informative.

        Reconciliation Records:
        ```json
        {records_string}
        ```
        Focus on identifying patterns and trends in the root causes. If possible, quantify the prevalence of each root cause (e.g., "Amount Mismatch accounted for 60% of discrepancies"). Be concise.
        """

        # Count tokens in the prompt template (excluding the records)
        prompt_template = prompt.replace(records_string, "")
        token_counts["prompt_template_tokens"] = count_tokens(prompt_template)
        
        # Calculate total input tokens
        token_counts["total_input"] = (
            token_counts["system_prompt"] +
            token_counts["records_tokens"] +
            token_counts["prompt_template_tokens"]
        )

        response = client.chat.completions.create(
            model="deepseek-ai/DeepSeek-V3",
            messages=[
                {"role": "system", "content": "You are a payment forensic analyst summarizing reconciliation data."},
                {"role": "user", "content": prompt}
            ]
        )

        summary = response.choices[0].message.content
        token_counts["response"] = count_tokens(summary)

        # Print token usage information
        print("\nToken Usage Breakdown:")
        print(f"System Prompt: {token_counts['system_prompt']} tokens")
        print(f"Records Data: {token_counts['records_tokens']} tokens")
        print(f"Prompt Template: {token_counts['prompt_template_tokens']} tokens")
        print(f"Response: {token_counts['response']} tokens")
        print(f"Total Input: {token_counts['total_input']} tokens")
        print(f"Total Tokens: {token_counts['total_input'] + token_counts['response']} tokens")

        return summary

    except Exception as e:
        error_message = f"Error generating summary: {e}"
        print(f"\nToken Usage (Error Case):")
        print(f"Input Tokens: {token_counts['total_input']}")
        error_tokens = count_tokens(error_message)
        print(f"Error Message Tokens: {error_tokens}")
        return error_message

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
    async with aiomysql.create_pool(
        host="127.0.0.1",
        user="app_user",
        password="app_password",
        port=3307,
        db='trading_platform',
        minsize=1,
        maxsize=10
    ) as pool:
        async with pool.acquire() as connection:
            async with connection.cursor() as cursor:
                try:
                    # 1. Check for unscanned transactions
                    await cursor.execute("""
                        SELECT * FROM transactions
                        WHERE transaction_id NOT IN (SELECT transaction_id FROM reconciliation_records)
                    """)
                    unscanned_transactions = await cursor.fetchall()

                    for transaction in unscanned_transactions:
                        transaction_id = transaction[0]

                        query = """
                            SELECT * FROM transactions WHERE transaction_id = %s
                        """

                        await cursor.execute(query, (transaction_id,))
                        transaction = await cursor.fetchone()

                        if not transaction:
                            raise HTTPException(status_code=404, detail="Transaction not found")
                        
                        query = """
                            SELECT * FROM payment_logs WHERE transaction_id = %s ORDER BY timestamp DESC LIMIT 1
                        """
                        await cursor.execute(query, (transaction_id,))
                        payment_log = await cursor.fetchone()

                        discrepancy_category = None
                        is_discrepancy = False
                        
                        if not payment_log:
                            discrepancy_category = "Missing Payments"
                            is_discrepancy = True
                        elif float(transaction[5]) != float(payment_log[5]):
                            discrepancy_category = "Amount Mismatch"
                            is_discrepancy = True
                        elif transaction[7] != payment_log[7]:
                            discrepancy_category = "Status Mismatch"
                            is_discrepancy = True

                        # Check for duplicate payments in the payment log
                        query = """
                            SELECT * FROM payment_logs WHERE transaction_id = %s
                        """
                        await cursor.execute(query, (transaction_id,))
                        payment_logs = await cursor.fetchall()
                        duplicate_payments = payment_logs if len(payment_logs) > 1 else []

                        if duplicate_payments and len(duplicate_payments) > 1:
                            discrepancy_category = "Duplicate Payment"
                            is_discrepancy = True
                        
                        root_cause = generate_llm_analysis(transaction, payment_log) if is_discrepancy else "No discrepancy detected"
                        
                        discrepancy_result = {
                            "transaction_id": transaction_id,
                            "is_discrepancy": is_discrepancy,
                            "discrepancy_category": discrepancy_category,
                            "root_cause": root_cause
                        }

                        # Get gateway status and amount
                        await cursor.execute("""
                            SELECT * FROM payment_logs
                            WHERE transaction_id = %s
                            ORDER BY timestamp DESC
                            LIMIT 1
                        """, (transaction[0],))
                        gateway_status_result = await cursor.fetchone()

                        gateway_status = gateway_status_result[4] if gateway_status_result else None
                        gateway_amount = gateway_status_result[5] if gateway_status_result else None

                        discrepancy_amount = abs(float(transaction[5]) - float(gateway_amount or 0)) if gateway_amount is not None else -1

                        reconciled_balance = gateway_amount if gateway_amount is not None else None

                        # Determine resolution status
                        if gateway_status == "Success" and transaction[7] == "Success":
                            resolution_status = 'No Discrepancy' if discrepancy_amount == 0 else 'Resolved'
                        else:
                            resolution_status = 'Unresolved'

                        if resolution_status == "Unresolved" or resolution_status == "No Discrepancy":
                            reconciled_balance = None  # Reset if not resolved

                        try:
                            insert_query = """
                                INSERT INTO reconciliation_records (
                                    reconciliation_id, transaction_id, discrepancy_category, transaction_date,
                                    payment_reference, amount, status, gateway_status, discrepancy_amount,
                                    root_cause, assigned_to, resolution_status, balance, reconciled_balance
                                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """

                            if discrepancy_result.get('root_cause', {}) == "No discrepancy detected":
                                root_cause = discrepancy_result.get('root_cause', {})
                            else:
                                root_cause = discrepancy_result.get('root_cause', {}).get('analysis', "")

                            await cursor.execute(insert_query, (
                                str(uuid.uuid4()), transaction[0], discrepancy_result.get('discrepancy_category'),
                                transaction[8], transaction[9], transaction[5],
                                transaction[7], gateway_status, discrepancy_amount,
                                root_cause, None, resolution_status,
                                transaction[5], reconciled_balance
                            ))
                            await connection.commit()
                            print("Data Inserted")

                        except Error as e:
                            print(f"Error processing transaction: {e}")
                            connection.rollback()  # Important: Rollback on error
                            raise # Reraise the exception after rollback

                        asyncio.create_task(generate_reconciliation_summary(transaction[0]))

                except Error as e:
                    print(f"check_and_update_discrepancies error: {e}")
                    connection.rollback()
                    raise


async def generate_reconciliation_summary(transaction_id=None):  # Add transaction_id parameter
    connection = get_db_connection()  # Open a new connection
    cursor = connection.cursor(dictionary=True)

    try:
        if transaction_id:  # Generate summary for a specific transaction
            cursor.execute("""
                SELECT * FROM reconciliation_records 
                WHERE transaction_id = %s 
                ORDER BY transaction_date DESC LIMIT 10
            """, (transaction_id,)) # Add WHERE clause
            last_10_records = cursor.fetchall()
        else:
            cursor.execute("SELECT * FROM reconciliation_records ORDER BY transaction_date DESC LIMIT 10")
            last_10_records = cursor.fetchall()

        if last_10_records: # Check if there are any records
            discrepancy_count = sum(1 for record in last_10_records if record['discrepancy_category'] is not None)
            resolved_count = sum(1 for record in last_10_records if record['resolution_status'] in ('Resolved', 'No Discrepancy'))
            resolution_rate = (resolved_count / len(last_10_records)) * 100 if last_10_records else 0

            summary_data = {
                'summary_id': str(uuid.uuid4()),
                'timestamp': datetime.now(),
                'total_transactions': len(last_10_records),  # Summarizing the selected records
                'discrepancy_count': discrepancy_count,
                'resolution_rate': resolution_rate,
            }

            insert_reconciliation_summary(summary_data)
        else:
            print("No records found for generating summary")

    except Error as e:
        print(f"Error generating summary: {e}")
        raise
    finally:
        cursor.close()
        connection.close()  # Close connection properly


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
            "resolved_transactions": resolved_count + 10,
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
        
class ReconciliationSummary(BaseModel):
    summary_id: str
    timestamp: datetime
    total_transactions: int
    discrepancy_count: int
    resolution_rate: float
    # Add other summary fields as needed

def insert_reconciliation_summary(summary_data: dict):
    connection = get_db_connection()
    cursor = connection.cursor()
    try:
        insert_query = """
            INSERT INTO reconciliation_summaries (
                summary_id, timestamp, total_transactions, discrepancy_count, resolution_rate
            ) VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (
            summary_data['summary_id'], summary_data['timestamp'], summary_data['total_transactions'],
            summary_data['discrepancy_count'], summary_data['resolution_rate']
        ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error inserting reconciliation summary: {e}")
    finally:
        cursor.close()
        connection.close()

@app.get("/reconciliation_summaries")
async def get_reconciliation_summaries(
    limit: int = Query(10, description="Number of summaries to retrieve")
):
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        # Get the last 'limit * 10' reconciliation records to provide context to the LLM
        cursor.execute(f"SELECT * FROM reconciliation_records ORDER BY transaction_date DESC LIMIT {limit * 10}")
        reconciliation_records = cursor.fetchall()

        llm_summary = await generate_llm_summary(reconciliation_records)
        return {"summary": llm_summary}  # Return only the LLM summary

    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error fetching reconciliation summaries: {str(e)}")
    finally:
        cursor.close()
        connection.close()

@app.on_event("startup")
async def startup_event():
    try:
        await create_reconciliation_summaries_table()
    except Exception as e:  # Catch exceptions from table creation
        print(f"Startup failed: {e}")

def fetch_four_tables():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="app_user",
            password="app_password",
            database="trading_platform",
            port=3307
        )
        cursor = conn.cursor()
          
        # Mapping database table names to readable categories
        table_mapping = {
            "crypto_payment_logs": "Cryptocurrency",
            "ewallet_payment_logs": "E-Wallet",
            "fpx_payment_logs": "FPX",
            "mobile_payment_logs": "Mobile Payment"
        }        
        results = []

        for table, category in table_mapping.items():
            query = f"SELECT * FROM {table} LIMIT 5;"
            cursor.execute(query)

            # Fetch column names
            columns = [desc[0] for desc in cursor.description]

            # Fetch rows and convert to dict
            rows = cursor.fetchall()
            results.append({category: [dict(zip(columns, row)) for row in rows]})

        cursor.close()
        conn.close()
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def fetch_three_tables():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="app_user",
            password="app_password",
            database="trading_platform",
            port=3307
        )
        cursor = conn.cursor()
          
        # Mapping database table names to readable categories
        table_mapping = {
            "crypto_payment_logs": "Cryptocurrency",
            "ewallet_payment_logs": "E-Wallet",
            "fpx_payment_logs": "FPX"
        }        
        results = []

        for table, category in table_mapping.items():
            query = f"SELECT * FROM {table} LIMIT 5;"
            cursor.execute(query)

            # Fetch column names
            columns = [desc[0] for desc in cursor.description]

            # Fetch rows and convert to dict
            rows = cursor.fetchall()
            results.append({category: [dict(zip(columns, row)) for row in rows]})

        cursor.close()
        conn.close()
        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def fetch_consolidated_data():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="app_user",
            password="app_password",
            database="trading_platform",
            port=3307
        )
        cursor = conn.cursor()

        query = "SELECT * FROM payment_logs LIMIT 5;"
        cursor.execute(query)

        # Fetch column names
        columns = [desc[0] for desc in cursor.description]
        # Fetch rows and return as list of dicts
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]
        
        return rows
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        if conn.is_connected():
            conn.close()
    
@app.get("/fetch_four_tables")
def get_four_tables():
    data = fetch_four_tables()
    return data

@app.get("/fetch_three_tables")
def get_three_tables():
    data = fetch_three_tables()
    return data
    
@app.get("/fetch_consolidated_table")
def get_consolidated_data():
    data = fetch_consolidated_data()
    return data

def create_table_if_not_exists(cursor, table_name, df):
    """Dynamically create a table based on CSV columns if it does not exist."""
    column_types = []
    
    for col in df.columns:
        col_name = col.strip().replace(" ", "_")  # Clean column name
        sample_value = df[col].dropna().astype(str).head(1).values
        
        # Determine column type
        if sample_value.size > 0:
            if sample_value[0].isdigit():
                column_type = "INT"
            else:
                column_type = "VARCHAR(255)"
        else:
            column_type = "VARCHAR(255)"  # Default type
        
        column_types.append(f"{col_name} {column_type}")

    columns_sql = ", ".join(column_types)
    create_table_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_sql});"
    
    cursor.execute(create_table_query)

def upload_csv_to_mysql(file: UploadFile):
    # try:
    #     conn = mysql.connector.connect(
    #         host="127.0.0.1",
    #         user="app_user",
    #         password="app_password",
    #         database="trading_platform",
    #         port=3307
    #     )
    #     cursor = conn.cursor()

    #     contents = file.file.read()
    #     try:
    #         df = pd.read_csv(io.StringIO(contents.decode("utf-8", errors="ignore")))
    #         # Convert time_stamp to MySQL-compatible datetime format
    #         if "time_stamp" in df.columns:
    #             try:
    #                 df["time_stamp"] = pd.to_datetime(df["time_stamp"], errors="coerce", format="%d/%m/%Y %H:%M")
    #                 df["time_stamp"] = df["time_stamp"].dt.strftime("%Y-%m-%d %H:%M:%S")  # Ensure correct MySQL format
    #             except Exception as e:
    #                 raise HTTPException(status_code=400, detail=f"Invalid datetime format in 'time_stamp': {str(e)}")

    #         # Drop rows where time_stamp conversion failed (optional)
    #         df.drop_duplicates(subset=["unique_id"], inplace=True)
    #         df.dropna(subset=["time_stamp"], inplace=True)
    #     except Exception as e:
    #         raise HTTPException(status_code=400, detail=f"CSV Format Error: {str(e)}")
        
    #     if df.empty:
    #         raise HTTPException(status_code=400, detail="CSV file is empty.")

    #     print("CSV Loaded Successfully:\n", df.head())  # Debugging log

    #     table_name = "mobile_payment_logs"

    #     df.columns = [col.strip().replace(" ", "_") for col in df.columns]

    #     create_table_if_not_exists(cursor, table_name, df)

    #     # Insert data into MySQL
    #     columns = ", ".join(df.columns)
    #     values_placeholder = ", ".join(["%s"] * len(df.columns))
    #     insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values_placeholder})"

        # for _, row in df.iterrows():
        #     cursor.execute(insert_query, tuple(row))

    #     conn.commit()
    #     conn.close()
    return {"message": "CSV uploaded successfully"}

    # except HTTPException as http_ex:
    #     raise http_ex  # Re-raise HTTP exceptions

    # except Exception as e:
    #     print("Error Occurred:", traceback.format_exc())  # Print full error traceback
    #     raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")

@app.post("/upload_csv")
def upload_csv(file: UploadFile = File(...)):
    return upload_csv_to_mysql(file)

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