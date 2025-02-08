from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import logging
import os
import json
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Forex API URL (set in environment variables)
FOREX_SENTIMENT_API_URL = os.getenv("FOREX_SENTIMENT_API_URL", "https://api.example.com/forex/sentiment")
API_KEY = os.getenv("API_KEY", "your_api_key_here")

# File path to save the sentiment data
SENTIMENT_FILE_PATH = os.getenv("SENTIMENT_FILE_PATH", "forex_sentiment.json")

# Load the forex pairs from the .env file
FOREX_PAIRS = os.getenv("FOREX_PAIRS", "USD/EUR,GBP/USD,AUD/USD").split(",")

# Function to fetch forex sentiment
def fetch_forex_sentiment():
    sentiment_data = {}  # Dictionary to hold sentiment data
    
    for pair in FOREX_PAIRS:
        try:
            response = requests.get(f"{FOREX_SENTIMENT_API_URL}/{pair}")
            response.raise_for_status()
            data = response.json()
            sentiment_data[pair] = data  # Store entire response data in the dictionary
            logging.info(f"Sentiment data for {pair}: {data}")
        except requests.exceptions.RequestException as e:
            logging.error(f"Error fetching sentiment for {pair}: {e}")
            sentiment_data[pair] = {"error": str(e)}

    # Save the entire sentiment data to a JSON file
    try:
        with open(SENTIMENT_FILE_PATH, "w") as json_file:
            json.dump(sentiment_data, json_file, indent=4)
        logging.info(f"Sentiment data saved to {SENTIMENT_FILE_PATH}")
    except Exception as e:
        logging.error(f"Error saving sentiment data to file: {e}")

# DAG definition with dynamic start_date
default_args = {
    "owner": "airflow",
    "start_date": datetime.now(),  # Set start date to the current time
    "retries": 1,
}

dag = DAG(
    "forex_sentiment_fetcher",
    default_args=default_args,
    schedule_interval="@hourly",  # Every hour
    catchup=False
)

fetch_sentiment_task = PythonOperator(
    task_id="fetch_forex_sentiment",
    python_callable=fetch_forex_sentiment,
    dag=dag
)