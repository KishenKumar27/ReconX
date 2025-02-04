import mysql.connector
import os
from dotenv import load_dotenv

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

# SQL queries to create tables
queries = [
    """
    CREATE TABLE User (
        user_id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) NOT NULL,
        email VARCHAR(100) NOT NULL,
        role VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """,
    """
    CREATE TABLE Trade (
        trade_id INT AUTO_INCREMENT PRIMARY KEY,
        trade_date TIMESTAMP NOT NULL,
        trade_price DECIMAL(10, 2) NOT NULL,
        trade_quantity INT NOT NULL,
        trade_status VARCHAR(50) NOT NULL,
        trader_id INT,
        broker_id INT,
        FOREIGN KEY (trader_id) REFERENCES User(user_id) ON DELETE SET NULL,
        FOREIGN KEY (broker_id) REFERENCES User(user_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE Dispute (
        dispute_id INT AUTO_INCREMENT PRIMARY KEY,
        trade_id INT,
        reported_by INT,
        dispute_description TEXT NOT NULL,
        dispute_type VARCHAR(50) NOT NULL,
        status VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        resolved_at TIMESTAMP,
        FOREIGN KEY (trade_id) REFERENCES Trade(trade_id) ON DELETE CASCADE,
        FOREIGN KEY (reported_by) REFERENCES User(user_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE Resolution (
        resolution_id INT AUTO_INCREMENT PRIMARY KEY,
        dispute_id INT,
        recommended_action TEXT NOT NULL,
        accepted_by INT,
        resolution_status VARCHAR(50) NOT NULL,
        resolved_at TIMESTAMP,
        FOREIGN KEY (dispute_id) REFERENCES Dispute(dispute_id) ON DELETE CASCADE,
        FOREIGN KEY (accepted_by) REFERENCES User(user_id) ON DELETE SET NULL
    );
    """,
    """
    CREATE TABLE Log (
        log_id INT AUTO_INCREMENT PRIMARY KEY,
        dispute_id INT,
        action VARCHAR(100) NOT NULL,
        performed_by INT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (dispute_id) REFERENCES Dispute(dispute_id) ON DELETE CASCADE,
        FOREIGN KEY (performed_by) REFERENCES User(user_id) ON DELETE SET NULL
    );
    """
]

# Execute each query
for query in queries:
    cursor.execute(query)
    print(f"Executed: {query[:30]}...")  # Print the first 30 characters of the query for feedback

# Commit the changes
db_connection.commit()

# Close the cursor and connection
cursor.close()
db_connection.close()

print("Tables created successfully.")
