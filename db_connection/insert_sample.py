import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()


# Database connection configuration
config = {
    'user': os.getenv("USER1"),  # Replace with your MySQL username
    'password': os.getenv("DB_PASSWORD"),  # Replace with your MySQL password
    'host': os.getenv("HOST"),  # Replace with your MySQL host
    'database': os.getenv("DATABASE"), # Replace with your database name
    'port': os.getenv("PORT")
}

# Function to establish a database connection
def create_connection():
    try:
        connection = mysql.connector.connect(**config)
        if connection.is_connected():
            print("Connected to MySQL database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# Function to insert forex sample data
def insert_forex_data(connection):
    cursor = connection.cursor()

    # Insert sample data into the User table
    users = [
        ("forex_trader", "trader@example.com", "trader"),
        ("forex_broker", "broker@example.com", "broker"),
        ("compliance_officer", "compliance@example.com", "compliance_officer")
    ]
    cursor.executemany(
        "INSERT INTO User (username, email, role) VALUES (%s, %s, %s)",
        users
    )
    print("Inserted data into User table")

    # Insert sample data into the Trade table
    trades = [
        (datetime(2023, 10, 15, 10, 15), 1.2000, 100000, "executed", 1, 2),
        (datetime(2023, 10, 16, 11, 30), 1.1950, 50000, "settled", 1, 2),
        (datetime(2023, 10, 17, 12, 45), 1.2100, 75000, "failed", 1, 2)
    ]
    cursor.executemany(
        "INSERT INTO Trade (trade_date, trade_price, trade_quantity, trade_status, trader_id, broker_id) VALUES (%s, %s, %s, %s, %s, %s)",
        trades
    )
    print("Inserted data into Trade table")

    # Insert sample data into the Dispute table
    disputes = [
        (1, 1, "Trade executed at incorrect exchange rate", "Trading's Hub", "pending"),
        (2, 1, "Settlement failed due to missing document", "Trading's Hub", "resolved")
    ]
    cursor.executemany(
        "INSERT INTO Dispute (trade_id, reported_by, dispute_description, dispute_type, status) VALUES (%s, %s, %s, %s, %s)",
        disputes
    )
    print("Inserted data into Dispute table")

    # Insert sample data into the Resolution table
    resolutions = [
        (1, "Re-execute trade at correct exchange rate", 3, "accepted", datetime(2023, 10, 16, 14, 0)),
        (2, "Request missing document and resettle", 3, "pending", None)
    ]
    cursor.executemany(
        "INSERT INTO Resolution (dispute_id, recommended_action, accepted_by, resolution_status, resolved_at) VALUES (%s, %s, %s, %s, %s)",
        resolutions
    )
    print("Inserted data into Resolution table")

    # Insert sample data into the Log table
    logs = [
        (1, "Dispute reported by forex_trader", 1),
        (1, "AI recommended re-execution", 3),
        (2, "Dispute reported by forex_trader", 1)
    ]
    cursor.executemany(
        "INSERT INTO Log (dispute_id, action, performed_by) VALUES (%s, %s, %s)",
        logs
    )
    print("Inserted data into Log table")

    # Commit the transaction
    connection.commit()
    print("Forex sample data inserted successfully")

    # Close the cursor
    cursor.close()

# Main function
def main():
    connection = create_connection()
    if connection:
        insert_forex_data(connection)
        connection.close()
        print("Database connection closed")

# Run the script
if __name__ == "__main__":
    main()
