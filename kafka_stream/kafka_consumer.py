from kafka import KafkaConsumer
import json
import boto3


# Connect to local Kafka broker
consumer = KafkaConsumer(
    "customer_feedback",
    bootstrap_servers="localhost:9092",
    auto_offset_reset="earliest",
    group_id="feedback-consumer-group",
    value_deserializer=lambda v: json.loads(v.decode("utf-8"))
)

print("Listening for messages...")

# DynamoDB setup
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('CustomerFeedback')

try:
    with table.batch_writer() as batch:
        for message in consumer:
            message = message.value
            # feedback_id = data.get(feedback_id,"")
            # category = data.get(category,"")
            # description = data.get(description,"")
            print(f"Read: {message}")

            batch.put_item(
                Item={
                    "feedback_category": message['category'],
                    "feedback_id": message['feedback_id'],
                    "description": message['description']
                }
            )

except KeyboardInterrupt:
    print("Stopping consumer...")
finally:
    consumer.close()
