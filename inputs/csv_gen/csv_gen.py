import pandas as pd
import random
from datetime import datetime, timedelta

num_transactions = 50
atm_ids = [101, 102, 103, 104, 105]
customer_ids = list(range(1, 51))  # assuming 50 customers from PSQL database
transaction_types = ["deposit", "withdrawal"]

data = []

for _ in range(num_transactions): # randomly generate transactions
    atm_id = random.choice(atm_ids)
    customer_id = random.choice(customer_ids)
    timestamp = datetime.now() - timedelta(days=random.randint(0,10), hours=random.randint(0,23))
    amount = round(random.uniform(20, 1000), 2)
    transaction_type = random.choice(transaction_types)
    
    data.append([atm_id, timestamp, amount, transaction_type, customer_id])

df = pd.DataFrame(data, columns=["atm_id", "timestamp", "amount", "transaction_type", "customer_id"])
df.to_csv("atm_activity.csv", index=False)
