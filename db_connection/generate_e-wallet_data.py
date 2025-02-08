import random
import uuid
import mysql.connector
from datetime import datetime, timedelta

# Define payment methods and statuses
payment_methods = ["GrabPay", "Touch 'n Go", "Boost", "ShopeePay", "BigPay"]
transaction_statuses = ["Processed", "In Progress", "Unsuccessful"]
transaction_categories = ["Top-up", "Payout"]

def generate_e_wallet_data(num_transactions=100):
    transactions = []
    start_date = datetime.now() - timedelta(days=30)
    
    for _ in range(num_transactions):
        transaction_id = str(uuid.uuid4())
        user_account = f"USR{random.randint(10000, 99999)}"
        payment_method = random.choice(payment_methods)
        transaction_value = round(random.uniform(10, 5000), 2)
        transaction_status = random.choice(transaction_statuses)
        transaction_category = random.choice(transaction_categories)
        transaction_time = start_date + timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        issue_flag = None
        
        # Introduce some issue flags
        if random.random() < 0.1:
            issue_flag = "Unrecorded Transaction"
        elif random.random() < 0.1:
            issue_flag = "Repeated Entry"
        
        transactions.append((transaction_id, user_account, payment_method, transaction_value, transaction_status, transaction_category, transaction_time, issue_flag))
    
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
    CREATE TABLE IF NOT EXISTS e_wallet_transactions (
        transaction_id VARCHAR(36) PRIMARY KEY,
        user_account VARCHAR(20),
        payment_method VARCHAR(50),
        transaction_value DECIMAL(10,2),
        transaction_status VARCHAR(20),
        transaction_category VARCHAR(20),
        transaction_time DATETIME
        )
    """
    cursor.execute(create_table_query)
    
    insert_query = """
    INSERT INTO e_wallet_transactions (transaction_id, user_account, payment_method, transaction_value, transaction_status, transaction_category, transaction_time)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    
    cursor.executemany(insert_query, data)
    conn.commit()
    cursor.close()
    conn.close()
    
    print("E-wallet transactions inserted into MySQL successfully!")

# Generate and insert data
data = generate_e_wallet_data()
insert_into_mysql(data)
