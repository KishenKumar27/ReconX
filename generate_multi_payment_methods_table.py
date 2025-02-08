from code_generator import StandardizeFormatCodeGenerator
from db_connection.db_utils import upload_to_mysql
import pandas as pd
import uuid

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

if __name__ == '__main__':
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
    
    