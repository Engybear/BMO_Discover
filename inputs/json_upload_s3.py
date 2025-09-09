import pandas as pd
from io import BytesIO
import boto3

# Acquire Dataframe
df = pd.read_json("./json_gen/credit_data.json")

# Convert data to Parquet and upload to S3 directly using a buffer
buffer = BytesIO()
df.to_parquet(buffer, engine="pyarrow", index=False)
buffer.seek(0)

s3 = boto3.client('s3')

s3.put_object(Bucket="customer-insights-input",
              Key="customers/credit_data.parquet",
              Body=buffer.getvalue())