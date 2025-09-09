import json
import random

loan_types = ["car", "house", "business", "student", "personal"]
num_customers = 50
credit_data = []

for customer_id in range(1, num_customers + 1):
    # Pick how many loans the customer has
    num_loans = random.randint(0, 3)
    loans = []
    
    for _ in range(num_loans):
        loan = {
            "type": random.choice(loan_types),
            "amount": round(random.uniform(1000, 100000), 2)
        }
        loans.append(loan)

    customer = {
        "customer_id": customer_id,
        "credit_score": random.randint(300, 850),
        "delinquencies": random.randint(0, 5),
        "outstanding_loans": loans
    }
    credit_data.append(customer)

# Save to JSON file
with open("credit_data.json", "w") as f:
    json.dump(credit_data, f, indent=4)
