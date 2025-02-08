import random
import uuid
import mysql.connector
from datetime import datetime, timedelta

# Define banks and statuses
banks = ["Maybank", "CIMB", "Public Bank", "RHB", "Hong Leong Bank", "AmBank", "Bank Islam"]
statuses = ["Successful", "Pending", "Failed"]
tx_types = ["Deposit", "Withdrawal"]

def generate_fpx_data(num_transactions=100):
    transactions = []
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(num_transactions):
        transaction_id = str(uuid.uuid4())
        account_id = f"ACC{random.randint(10000, 99999)}"
        bank = random.choice(banks)
        amount = round(random.uniform(10, 5000), 2)
        status = random.choice(statuses)
        tx_type = random.choice(tx_types)
        timestamp = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        discrepancy = None
        
        # Introduce some discrepancies
        if random.random() < 0.1:
            discrepancy = "Missing Payment"
        elif random.random() < 0.1:
            discrepancy = "Duplicate Transaction"
        
        transactions.append((transaction_id, account_id, bank, amount, status, tx_type, timestamp, discrepancy))
    
    return transactions

# Connect to MySQL
def insert_into_mysql(data):
    conn = mysql.connector.connect(
        host="10.10.240.93",
        user="app_user",
        password="app_password",
        database="payment_resolution",
        port=3306
    )
    cursor = conn.cursor()
    
    create_table_query = """
    CREATE TABLE IF NOT EXISTS fpx_transactions (
        transaction_id VARCHAR(36) PRIMARY KEY,
        account_id VARCHAR(20),
        bank VARCHAR(50),
        amount DECIMAL(10,2),
        status VARCHAR(20),
        transaction_type VARCHAR(20),
        timestamp DATETIME
        )
    """
    cursor.execute(create_table_query)
    
    insert_query = """
    INSERT INTO fpx_transactions (transaction_id, account_id, bank, amount, status, transaction_type, timestamp)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    
    print("Data inserted into MySQL successfully!")

# Generate and insert data
data = generate_fpx_data()
insert_into_mysql(data)
