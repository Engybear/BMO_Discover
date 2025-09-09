from kafka import KafkaProducer
import json
import random
import time
import uuid
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

complaints = {
    "ATM Issue": [
        "ATM out of service",
        "Unable to withdraw cash",
        "Deposit slot jammed"
    ],
    "Account Problem": [
        "Incorrect balance",
        "Unauthorized transaction",
        "Account locked"
    ],
    "Card Issue": [
        "Card not recognized",
        "Card swallowed by ATM",
        "Card expired unexpectedly"
    ],
    "Service Feedback": [
        "Long waiting time",
        "Poor customer service",
        "Staff unavailable"
    ]
}

topic = "customer_feedback"

try:
    while True:
        # Pick random category
        category = random.choice(list(complaints.keys()))
        # Pick random description from that category
        description = random.choice(complaints[category])

        feedback_id = str(uuid.uuid4())
        print(feedback_id)

        message = {
            "feedback_id":feedback_id,
            "category": category,
            "description": description
        }

        producer.send(topic, value=message)
        print(f"Produced: {message}")
        producer.flush()

        time.sleep(5)

except KeyboardInterrupt:
    print("Producer stopped.")
finally:
    producer.close()