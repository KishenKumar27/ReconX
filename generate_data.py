import random
import uuid
from datetime import datetime, timedelta
import pandas as pd
import mysql.connector
from dataclasses import dataclass

@dataclass
class GenerationConfig:
    """Configuration for data generation"""
    num_transactions: int = 10
    refund_probability: float = 0.2  # Probability of a transaction having a refund
    pending_probability: float = 0.2  # Probability of a transaction being pending
    days_range: int = 30  # Range of days in the past for transaction dates
    processing_fee_percentage: float = 0.02  # 2% processing fee

    # Sample data pools
    users: list = None
    payment_methods: list = None
    currencies: list = None
    transaction_statuses: list = None
    gateway_statuses: list = None
    reconciliation_statuses: list = None
    refund_reasons: list = None
    audit_actions: list = None

    def __post_init__(self):
        # Initialize default values if none provided
        self.users = self.users or ["user_1", "user_2", "user_3", "user_4", "user_5"]
        self.payment_methods = self.payment_methods or ["Bank Transfer", "Crypto", "E-Wallet", "Credit Card"]
        self.currencies = self.currencies or ["USD", "MYR", "BTC"]
        self.transaction_statuses = self.transaction_statuses or ["Pending", "Success", "Failed", "Cancelled"]
        self.gateway_statuses = self.gateway_statuses or ["Pending", "Success", "Failed"]
        self.reconciliation_statuses = self.reconciliation_statuses or ["Matched", "Unmatched", "Partial"]
        self.refund_reasons = self.refund_reasons or ["Fraudulent", "Duplicate", "Customer Dispute", "Bank Error"]
        self.audit_actions = self.audit_actions or [
            "Transaction Created", "Transaction Updated", 
            "Refund Processed", "Chargeback Issued"
        ]

@dataclass
class DBConfig:
    """Database connection configuration"""
    host: str = "localhost"
    user: str = "root"
    password: str = "strong_password"
    port: str = "3307"
    database: str = "trading_platform"

def create_database(db_config: DBConfig):
    """Create the trading_platform database if it doesn't exist."""
    conn = mysql.connector.connect(
        host=db_config.host,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port
    )
    cursor = conn.cursor()
    
    cursor.execute(f"DROP DATABASE {db_config.database}")

    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_config.database}")
    
    cursor.close()
    conn.close()

def create_tables(cursor):
    # Create transactions table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS transactions (
        transaction_id VARCHAR(36) PRIMARY KEY,
        user_id VARCHAR(50),
        account_id VARCHAR(50),
        payment_method VARCHAR(50),
        transaction_type VARCHAR(20),
        amount DECIMAL(15, 2),
        currency VARCHAR(10),
        transaction_status VARCHAR(20),
        transaction_date DATETIME,
        payment_reference VARCHAR(50),
        processing_fee DECIMAL(15, 2),
        net_amount DECIMAL(15, 2),
        remarks TEXT
    )
    """)

    # Create payment_logs table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS payment_logs (
        log_id VARCHAR(36) PRIMARY KEY,
        transaction_id VARCHAR(36),
        gateway_name VARCHAR(100),
        gateway_transaction_id VARCHAR(100),
        gateway_status VARCHAR(20),
        gateway_amount DECIMAL(15, 2),
        gateway_currency VARCHAR(10),
        gateway_response TEXT,
        timestamp DATETIME,
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    )
    """)

    # Create reconciliation_records table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS reconciliation_records (
        reconciliation_id VARCHAR(36) PRIMARY KEY,
        transaction_id VARCHAR(36),
        discrepancy_category VARCHAR(50),
        transaction_date DATETIME,
        payment_reference VARCHAR(50),
        amount DECIMAL(15, 2),
        status VARCHAR(20),
        gateway_status VARCHAR(20),
        discrepancy_amount DECIMAL(15, 2),
        root_cause LONGTEXT,
        assigned_to VARCHAR(50),
        resolution_status VARCHAR(20),
        balance DECIMAL(15, 2),
        reconciled_balance DECIMAL(15, 2),
        FOREIGN KEY (transaction_id) REFERENCES transactions(transaction_id)
    )
    """)


def generate_transactions(config: GenerationConfig):
    transactions = []
    for _ in range(config.num_transactions):
        transaction_id = str(uuid.uuid4())
        user_id = random.choice(config.users)
        account_id = f"acc_{random.randint(1000, 9999)}"
        payment_method = random.choice(config.payment_methods)
        transaction_type = random.choice(["Deposit", "Withdrawal"])
        amount = round(random.uniform(100, 5000), 2)
        currency = random.choice(config.currencies)
        status = "Pending" if random.random() < config.pending_probability else "Success"
        transaction_date = datetime.now() - timedelta(days=random.randint(1, config.days_range))
        payment_reference = str(uuid.uuid4())[:10]
        processing_fee = round(amount * config.processing_fee_percentage, 2)
        net_amount = amount - processing_fee
        
        transactions.append([
            transaction_id, user_id, account_id, payment_method, transaction_type,
            amount, currency, status, transaction_date, payment_reference,
            processing_fee, net_amount, ""
        ])
    return transactions

def generate_payment_logs(transactions, config: GenerationConfig):
    logs = []
    discrepancies = []
    missing_payments = []
    payment_references = set()
    duplicate_payment_transactions = []
    transactions_without_discrepancy = []

    for tx in transactions:
        is_discrepancy = False
        if tx[7] == "Success":  # Only Success transactions have gateway logs
            if random.random() < 0.2:  # 20% chance of missing payment
                missing_payments.append(tx[0])
                is_discrepancy = True
                continue

            log_id = str(uuid.uuid4())
            gateway_name = "Payment Gateway X"
            gateway_transaction_id = str(uuid.uuid4())
            gateway_status = "Success"
            gateway_amount = tx[5]
            
            # Introduce discrepancy: payment log amount may not match transaction amount
            if random.random() < 0.2:  # 20% chance of amount mismatch
                amount_discrepancy = round(gateway_amount * random.uniform(0.01, 0.1), 2)  # 1% to 10% discrepancy
                gateway_amount += amount_discrepancy
                discrepancies.append((tx[0], amount_discrepancy))
                is_discrepancy = True

            # Introduce discrepancy: status mismatch
            if random.random() < 0.2:  # 20% chance of status mismatch
                gateway_status = "Pending"
                discrepancies.append((tx[0], "Status mismatch"))
                is_discrepancy = True

            # Introduce discrepancy: duplicate payment reference
            if gateway_status == "Success" and random.random() < 0.2:
                duplicate_payment_transactions.append(tx[0])
                discrepancies.append((tx[0], "Duplicate payment"))
                is_discrepancy = True
            payment_references.add(tx[9])

            gateway_currency = tx[6]
            gateway_response = "Success"
            timestamp = tx[8] + timedelta(minutes=random.randint(1, 60))
            
            logs.append([
                log_id, tx[0], gateway_name, gateway_transaction_id,
                gateway_status, gateway_amount, gateway_currency,
                gateway_response, timestamp
            ])

            if not is_discrepancy:
                transactions_without_discrepancy.append(tx[0])

    print("\nTransactions with discrepancies:")
    for tx_id, discrepancy in discrepancies:
        print(f"Transaction ID: {tx_id}, Discrepancy: {discrepancy}")

    print("\nMissing payments:")
    for tx_id in missing_payments:
        print(f"Transaction ID: {tx_id}")

    print("\nDuplicate payments:")
    for tx_id in duplicate_payment_transactions:
        print(f"Transaction ID: {tx_id}")

    print("\nTransactions without discrepancies:")
    for tx_id in transactions_without_discrepancy:
        print(f"Transaction ID: {tx_id}")

    return logs


def push_to_mysql(transactions, payment_logs, db_config: DBConfig):
    create_database(db_config)
    
    conn = mysql.connector.connect(
        host=db_config.host,
        user=db_config.user,
        password=db_config.password,
        port=db_config.port,
        database=db_config.database
    )
    cursor = conn.cursor()
    
    # Create tables first
    create_tables(cursor)
    
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
    
    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    # Create configuration objects with default or custom values
    gen_config = GenerationConfig(
        num_transactions=100,  # Generate 100 transactions
        refund_probability=0.3,  # 30% chance of refund
        pending_probability=0.15,  # 15% chance of pending status
        days_range=60,  # Transactions from last 60 days
        processing_fee_percentage=0.025  # 2.5% processing fee
    )
    
    db_config = DBConfig(
        host="localhost",
        user="root",
        password="strong_password",
        port="3307",
        database="trading_platform"
    )
    
    # Generate data
    transactions = generate_transactions(gen_config)
    payment_logs = generate_payment_logs(transactions, gen_config)
    
    # Push to MySQL
    push_to_mysql(transactions, payment_logs, db_config)