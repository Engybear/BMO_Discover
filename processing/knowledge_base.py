import boto3
from io import BytesIO
import pandas as pd
import json
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, ArrayType, FloatType, IntegerType, LongType, DoubleType
from pyspark.sql.functions import col, to_timestamp
from pyspark.sql.functions import collect_list, struct

# Initialize Spark and Hadoop
spark = SparkSession.builder \
    .appName("BankDataETL") \
    .config("spark.hadoop.hadoop.metrics.conf", 
        "C:\\hadoop\\hadoop-3.4.1\\etc\\hadoop\\hadoop-metrics2.properties") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.driver.extraJavaOptions", "-Dorg.apache.hadoop.io.nativeio.NativeIO.disable=true") \
    .config("spark.executor.extraJavaOptions", "-Dorg.apache.hadoop.io.nativeio.NativeIO.disable=true") \
    .config("spark.hadoop.io.nativeio.enabled", "false") \
    .getOrCreate()

hadoop_conf = spark._jsc.hadoopConfiguration()
hadoop_conf.set("fs.s3a.access.key", "ACCESS_KEY_HERE")
hadoop_conf.set("fs.s3a.secret.key", "SECRET_ACCESS_KEY_HERE")
hadoop_conf.set("fs.s3a.endpoint", "s3.amazonaws.com")

# Read Parquet files from S3
combined = spark.read.parquet("s3a://customer-insights-input/processed/combined/part-00000-8b6842e8-f729-4f88-8554-c4269354a618-c000.snappy.parquet")

# Write to buffer
buffer = BytesIO()
for row_json in combined.toJSON().toLocalIterator():
    buffer.write((row_json + "\n").encode("utf-8"))
buffer.seek(0)

s3 = boto3.client('s3')
s3.put_object(Bucket="customer-insights-input",
              Key="processed/rag-knowledge-base/combined.JSON",
              Body=buffer.getvalue())


spark.stop()

print("Completed processing")
