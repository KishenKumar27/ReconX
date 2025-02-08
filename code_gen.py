import pandas as pd
import uuid
import mysql.connector
from mysql.connector import Error 

def upload_to_mysql(dataframe, table_name):
    try:
        db_config = {
            'host': '10.10.240.93',
            'user': 'app_user',
            'password': 'app_password',
            'database': 'payment_resolution',
            'port': 3306
        }
        
        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(**db_config)
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            log_id VARCHAR(36) PRIMARY KEY,
            transaction_id VARCHAR(255),
            user_id VARCHAR(255),
            payment_method VARCHAR(255),
            amount DECIMAL(15, 2),
            status VARCHAR(50),
            timestamp DATETIME
        );
        """
        cursor.execute(create_table_query)

        # Insert data into the table
        insert_query = f"""
        INSERT INTO {table_name} (log_id, transaction_id, user_id, payment_method, amount, status, timestamp)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        
        delete_query = f"DELETE FROM {table_name} WHERE status = 'Duplicate';"
        
        # Convert DataFrame to a list of tuples
        data_tuples = [
            (
                str(row["log_id"]),
                str(row["transaction_id"]),
                str(row["user_id"]),
                str(row["payment_method"]),
                float(row["amount"]) if pd.notna(row["amount"]) else None,
                str(row["status"]),
                row["timestamp"] if pd.notna(row["timestamp"]) else None
            )
            for _, row in dataframe.iterrows()
        ]

        # Execute batch insert for better performance
        cursor.executemany(insert_query, data_tuples)
        
        # Commit the transaction
        connection.commit()
        print(f"Data uploaded to {table_name} successfully!")
        
        # Execute batch insert for better performance
        cursor.execute(delete_query)
        
        # Commit the transaction
        connection.commit()
        print(f"Data deleted from {table_name} successfully!")

    except Error as e:
        print(f"Error: {e}")
    
    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

def standardize_dataset(dataset):
    # Define mappings for columns and values
    column_mappings = {
        'crypto_payments_table': {
            'transaction_id': 'transaction_id',
            'gateway_status': 'status',
            'gateway_amount': 'amount',
            'timestamp': 'timestamp'
        },
        'e_wallet_transactions_table': {
            'transaction_id': 'transaction_id',
            'user_account': 'user_id',
            'payment_method': 'payment_method',
            'transaction_value': 'amount',
            'transaction_status': 'status',
            'transaction_time': 'timestamp'
        },
        'fpx_transactions_table': {
            'transaction_id': 'transaction_id',
            'account_id': 'user_id',
            'bank': 'payment_method',
            'amount': 'amount',
            'status': 'status',
            'timestamp': 'timestamp'
        }
    }

    value_mappings = {
        'status': {
            'Success': 'Success',
            'Processed': 'Success',
            'Completed': 'Success',
            'Unsuccessful': 'Failed',
            'In Progress': 'Pending',
            "Reversed": 'Failed'
        }
    }

    # Apply column mappings
    standardized_data = dataset.rename(columns=column_mappings.get(dataset.name, {}))

    # Apply value mappings
    for col, mapping in value_mappings.items():
        if col in standardized_data.columns:
            standardized_data[col] = standardized_data[col].replace(mapping)

    return standardized_data

# Example usage
if __name__ == "__main__":
    crypto_payments = pd.read_csv('./crypto.csv')
    e_wallet_transactions = pd.read_csv('./e-wallet.csv')
    fpx_transactions = pd.read_csv('./fpx.csv')

    crypto_payments.name = 'crypto_payments_table'
    e_wallet_transactions.name = 'e_wallet_transactions_table'
    fpx_transactions.name = 'fpx_transactions_table'

    standardized_crypto = standardize_dataset(crypto_payments)
    standardized_e_wallet = standardize_dataset(e_wallet_transactions)
    standardized_fpx = standardize_dataset(fpx_transactions)

    # Combine standardized datasets
    final_dataset = pd.concat([standardized_crypto, standardized_e_wallet, standardized_fpx])
    # Generate a random log_id for each row
    final_dataset['log_id'] = [str(uuid.uuid4()) for _ in range(len(final_dataset))]

    upload_to_mysql(final_dataset, 'payment')