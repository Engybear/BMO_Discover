import psycopg2
import pandas as pd
from io import BytesIO
import boto3

# Connect to Postgres
conn = psycopg2.connect(
    host="localhost",
    database="banking_data",
    user="postgres",
    password="DB_PASSWORD_HERE"
)

# Query data into a DataFrame
query = "SELECT * FROM customers;"
df = pd.read_sql(query, conn)

# Close connection to Postgres (no longer needed)
conn.close()

# Convert data to Parquet and upload to S3 directly using a buffer
buffer = BytesIO()
df.to_parquet(buffer, engine="pyarrow", index=False)
buffer.seek(0)

s3 = boto3.client('s3')

s3.put_object(Bucket="customer-insights-input",
              Key="customers/customers.parquet",
              Body=buffer.getvalue())