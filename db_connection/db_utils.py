import mysql.connector
import os
from dotenv import load_dotenv
import time

load_dotenv()

# Establish connection to MySQL
db_connection = mysql.connector.connect(
    host=os.getenv("HOST"),  # Replace with your host (e.g., localhost or IP address)
    user=os.getenv("USER1"),  # Replace with your database username
    password=os.getenv("DB_PASSWORD"),  # Replace with your database password
    database=os.getenv("DATABASE"),  # Replace with your database name
    port=os.getenv("PORT")  # Replace with your database port (e.g., 3306)
)

cursor = db_connection.cursor()

def insert_or_update_dispute(trade_id, reported_by, dispute_description, status, created_at, dispute_type=None, resolved_at=None):
    try:
        # Check if trade_id exists
        check_query = "SELECT COUNT(*) FROM Dispute WHERE trade_id = %s"
        cursor.execute(check_query, (trade_id,))
        exists = cursor.fetchone()[0] > 0

        if exists:
            # Update existing row
            update_query = """
            UPDATE Dispute 
            SET reported_by = %s, dispute_description = %s, dispute_type = %s, status = %s, created_at = %s, resolved_at = %s
            WHERE trade_id = %s
            """
            cursor.execute(update_query, (reported_by, dispute_description, dispute_type, status, created_at, resolved_at, trade_id))
        else:
            # Insert new row
            insert_query = """
            INSERT INTO Dispute (trade_id, reported_by, dispute_description, dispute_type, status, created_at, resolved_at)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (trade_id, reported_by, dispute_description, dispute_type, status, created_at, resolved_at))

        db_connection.commit()
        print("Dispute record inserted or updated successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
def insert_log(dispute_id, action, performed_by, timestamp=None):
    try:
        query = """
        INSERT INTO Log (dispute_id, action, performed_by, timestamp)
        VALUES (%s, %s, %s, %s);
        """
        
        cursor.execute(query, (dispute_id, action, performed_by, timestamp))
        db_connection.commit()
        print("Log record inserted successfully.")
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        
# Function to fetch new logs based on dispute_id
def fetch_logs(last_timestamp, dispute_id):
    cursor = None  # Initialize cursor here to prevent UnboundLocalError
    retries = 3  # Limit the number of retries
    attempt = 0
    
    while attempt < retries:
        try:
            if db_connection.is_connected():
                cursor = db_connection.cursor(dictionary=True)  # Ensure this returns dictionaries

                query = """
                SELECT dispute_id, action, timestamp FROM Log 
                WHERE dispute_id = %s AND timestamp > %s ORDER BY timestamp ASC;
                """
                cursor.execute(query, (dispute_id, last_timestamp))
                logs = cursor.fetchall()  # This should return a list of dictionaries
                return logs
            else:
                print("MySQL connection is closed. Attempting to reconnect...")
                db_connection.ping(reconnect=True, attempts=3, delay=5)  # Reconnect to MySQL
                attempt += 1
                time.sleep(2)  # Adding delay between retries
        except mysql.connector.errors.OperationalError as e:
            print(f"Database error: {e}")
            attempt += 1
            time.sleep(2)  # Adding delay between retries
        finally:
            if cursor:
                cursor.close()  # Close cursor only if it's defined