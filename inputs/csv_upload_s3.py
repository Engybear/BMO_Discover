import pandas as pd
from io import BytesIO
import boto3

# Acquire Dataframe
df = pd.read_csv("./csv_gen/atm_activity.csv")
df['amount'] = df['amount'].fillna(0)

# Convert data to Parquet and upload to S3 directly using a buffer
buffer = BytesIO()
df.to_parquet(buffer, engine="pyarrow", index=False)
buffer.seek(0)

s3 = boto3.client('s3')

s3.put_object(Bucket="customer-insights-input",
              Key="customers/atm_activity.parquet",
              Body=buffer.getvalue())