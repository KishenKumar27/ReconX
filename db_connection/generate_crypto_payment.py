import random
import uuid
import mysql.connector
from datetime import datetime, timedelta

# MySQL Database Configuration
DB_CONFIG = {
    "host": "10.10.240.93",
    "user": "app_user",
    "password": "app_password",
    "database": "payment_resolution",
    "port": 3306
}

# Cryptocurrency options
CRYPTOCURRENCIES = ["BTC", "ETH", "USDT", "BNB", "XRP"]

# Payment statuses
STATUSES = ["Completed", "Pending", "Failed", "Reversed", "Duplicate"]

# Generate synthetic cryptocurrency payment transactions
def generate_transactions(num=100):
    transactions = []
    base_time = datetime.now() - timedelta(days=30)  # Random transactions in the last 30 days
    
    for _ in range(num):
        tx_id = str(uuid.uuid4())
        user_id = random.randint(1000, 5000)  # Simulating user IDs
        crypto = random.choice(CRYPTOCURRENCIES)
        amount = round(random.uniform(10, 5000), 2)
        tx_type = random.choice(["Deposit", "Withdrawal"])
        status = random.choices(STATUSES, weights=[80, 10, 5, 3, 2])[0]  # Higher probability for "Completed"
        timestamp = base_time + timedelta(seconds=random.randint(0, 2592000))  # Within 30 days
        
        transactions.append((tx_id, user_id, crypto, amount, tx_type, status, timestamp))
    
    return transactions

# Insert data into MySQL
def insert_transactions(transactions):
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS crypto_payments (
                id VARCHAR(36) PRIMARY KEY,
                user_id INT,
                cryptocurrency VARCHAR(10),
                amount DECIMAL(10, 2),
                transaction_type VARCHAR(10),
                status VARCHAR(15),
                timestamp DATETIME
            )
        """)
        
        insert_query = """
            INSERT INTO crypto_payments (id, user_id, cryptocurrency, amount, transaction_type, status, timestamp)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        cursor.executemany(insert_query, transactions)
        conn.commit()
        
        print(f"Inserted {len(transactions)} transactions successfully.")
    except mysql.connector.Error as e:
        print(f"Error: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    transactions = generate_transactions(100)
    insert_transactions(transactions)
