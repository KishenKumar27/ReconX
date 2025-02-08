import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector

# Sample users and payment methods
users = ["user_1", "user_2", "user_3", "user_4", "user_5"]
payment_methods = ["Bank Transfer", "Crypto", "E-Wallet", "Credit Card"]
currencies = ["USD", "MYR", "BTC"]
transaction_statuses = ["Pending", "Completed", "Failed", "Cancelled"]
gateway_statuses = ["Pending", "Success", "Failed"]
reconciliation_statuses = ["Matched", "Unmatched", "Partial"]
refund_reasons = ["Fraudulent", "Duplicate", "Customer Dispute", "Bank Error"]
audit_actions = ["Transaction Created", "Transaction Updated", "Refund Processed", "Chargeback Issued"]

# Generate sample transactions
def generate_transactions(n=10):
    transactions = []
    for _ in range(n):
        transaction_id = str(uuid.uuid4())
        user_id = random.choice(users)
        account_id = f"acc_{random.randint(1000, 9999)}"
        payment_method = random.choice(payment_methods)
        transaction_type = random.choice(["Deposit", "Withdrawal"])
        amount = round(random.uniform(100, 5000), 2)
        currency = random.choice(currencies)
        status = "Pending" if random.random() < 0.2 else "Completed"
        transaction_date = datetime.now() - timedelta(days=random.randint(1, 30))
        payment_reference = str(uuid.uuid4())[:10]
        processing_fee = round(amount * 0.02, 2)
        net_amount = amount - processing_fee
        
        transactions.append([
            transaction_id, user_id, account_id, payment_method, transaction_type,
            amount, currency, status, transaction_date, payment_reference,
            processing_fee, net_amount, ""
        ])
    return transactions

# Generate sample payment gateway logs
def generate_payment_logs(transactions):
    logs = []
    for tx in transactions:
        if tx[7] == "Completed":  # Only completed transactions go to gateway logs
            log_id = str(uuid.uuid4())
            gateway_name = "Payment Gateway X"
            gateway_transaction_id = str(uuid.uuid4())
            gateway_status = "Success"
            gateway_amount = tx[5]
            gateway_currency = tx[6]
            gateway_response = "Success"
            timestamp = tx[8] + timedelta(minutes=random.randint(1, 60))
            
            logs.append([
                log_id, tx[0], gateway_name, gateway_transaction_id,
                gateway_status, gateway_amount, gateway_currency,
                gateway_response, timestamp
            ])
    return logs

# Generate reconciliation records
def generate_reconciliation_records(transactions, payment_logs):
    reconciliations = []
    payment_log_map = {log[1]: log for log in payment_logs}
    
    for tx in transactions:
        reconciliation_id = str(uuid.uuid4())
        gateway_log = payment_log_map.get(tx[0])
        
        if gateway_log:
            matched_status = "Matched"
            discrepancy_amount = 0.00
            discrepancy_reason = ""
        else:
            matched_status = "Unmatched"
            discrepancy_amount = tx[5]
            discrepancy_reason = "Payment not found"
        
        reconciliations.append([
            reconciliation_id, tx[0], gateway_log[3] if gateway_log else "N/A",
            matched_status, discrepancy_amount, discrepancy_reason,
            "system", datetime.now()
        ])
    return reconciliations

# Generate refund and chargeback records
def generate_refund_chargebacks(transactions):
    refunds = []
    for tx in transactions:
        if random.random() < 0.2:  # 20% of transactions may have refunds/chargebacks
            refund_id = str(uuid.uuid4())
            transaction_id = tx[0]
            refund_amount = round(tx[5] * random.uniform(0.5, 1), 2)
            refund_reason = random.choice(refund_reasons)
            refund_status = random.choice(["Approved", "Rejected", "Pending"])
            refund_date = tx[8] + timedelta(days=random.randint(1, 10))
            
            refunds.append([
                refund_id, transaction_id, refund_amount, refund_reason, refund_status, refund_date
            ])
    return refunds

# Generate audit logs
def generate_audit_logs(transactions):
    logs = []
    for tx in transactions:
        audit_id = str(uuid.uuid4())
        transaction_id = tx[0]
        action = random.choice(audit_actions)
        performed_by = "system"
        timestamp = datetime.now() - timedelta(days=random.randint(1, 30))
        
        logs.append([
            audit_id, transaction_id, action, performed_by, timestamp
        ])
    return logs

# Push data to MySQL
def push_to_mysql(transactions, payment_logs, reconciliation_records, refunds, audit_logs):
    conn = mysql.connector.connect(
        host="127.0.0.1",
        user="root",
        password="root_password",
        port=3307,
        database="dispute_resolution_db"
    )
    cursor = conn.cursor()
    
    # Insert transactions
    cursor.executemany(
        """INSERT INTO transactions (
        transaction_id, user_id, account_id, payment_method, transaction_type,
        amount, currency, transaction_status, transaction_date, payment_reference,
        processing_fee, net_amount, remarks) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        transactions
    )
    
    # Insert payment logs
    cursor.executemany(
        """INSERT INTO payment_logs (
        log_id, transaction_id, gateway_name, gateway_transaction_id,
        gateway_status, gateway_amount, gateway_currency,
        gateway_response, timestamp) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)""",
        payment_logs
    )
    
    # Insert reconciliation records
    cursor.executemany(
        """INSERT INTO reconciliation_records (
        reconciliation_id, transaction_id, gateway_transaction_id, matched_status,
        discrepancy_amount, discrepancy_reason, reconciled_by, reconciliation_date) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        reconciliation_records
    )
    
    # Insert refund and chargeback records
    cursor.executemany(
        "INSERT INTO refund_chargebacks (refund_id, transaction_id, refund_amount, refund_reason, refund_status, refund_date) VALUES (%s, %s, %s, %s, %s, %s)",
        refunds
    )
    
    # Insert audit logs
    cursor.executemany(
        "INSERT INTO audit_logs (audit_id, transaction_id, action, performed_by, timestamp) VALUES (%s, %s, %s, %s, %s)",
        audit_logs
    )
    
    conn.commit()
    cursor.close()
    conn.close()

# Generate data
transactions = generate_transactions(10)
payment_logs = generate_payment_logs(transactions)
reconciliation_records = generate_reconciliation_records(transactions, payment_logs)
refunds = generate_refund_chargebacks(transactions)
audit_logs = generate_audit_logs(transactions)

# Push to MySQL
push_to_mysql(transactions, payment_logs, reconciliation_records, refunds, audit_logs)
