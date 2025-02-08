import pandas as pd
import random
import uuid
from faker import Faker

# Initialize Faker
fake = Faker()

# Define possible values for each column
mobile_payment_providers = ["Vodafone", "Airtel", "Tpaga", "Equitel", "OrangeMoney"]
transaction_types = ["Deposit", "Withdrawal"]
statuses = ["Completed", "Pending", "Reversed"]

# Generate 100 rows of data
data = []
for _ in range(100):
    transaction = {
        "mobile_id": str(uuid.uuid4()),
        "id": random.randint(1000, 5000),
        "mobile_payment": random.choice(mobile_payment_providers),
        "monetary": round(random.uniform(10, 5000), 2),
        "type": random.choice(transaction_types),
        "status": random.choice(statuses),
        "timestamp": fake.date_time_between(start_date="-1y", end_date="now").strftime("%Y-%m-%d %H:%M:%S")
    }
    data.append(transaction)

# Create DataFrame
df = pd.DataFrame(data)
df.to_csv("create_mobile_payment.csv", index=False)


# Display DataFrame
