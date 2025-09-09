import boto3
from io import BytesIO
import pandas as pd
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

schema_credit = StructType([
    StructField("customer_id", LongType(), True),
    StructField("credit_score", LongType(), True),
    StructField("delinquencies", LongType(), True),
    StructField("outstanding_loans", ArrayType(StructType([
        StructField("type", StringType(), True),
        StructField("amount", DoubleType(), True)
    ])), True)
])

# Read Parquet files from S3
customers = spark.read.parquet("s3a://customer-insights-input/customers/customers.parquet")
atm_activity = spark.read.parquet("s3a://customer-insights-input/customers/atm_activity.parquet")
credit_data  = spark.read.schema(schema_credit).parquet("s3a://customer-insights-input/customers/credit_data.parquet")

# aggregate atm activity by customer_id
atm_activity = atm_activity.withColumn("timestamp", to_timestamp(col("timestamp")))

atm_agg = atm_activity.groupBy("customer_id").agg(
    collect_list(
        struct("atm_id", "timestamp", "amount", "transaction_type")
    ).alias("atm_transactions")
)

# join datasets by customer_id
combined = customers.join(credit_data, "customer_id", "left") \
                    .join(atm_agg, "customer_id", "left")
# combined.printSchema()
# combined.show(5)

# Write combined data back to S3 for staging
combined.coalesce(1).write.mode("overwrite").parquet("s3a://customer-insights-input/processed/combined/")

spark.stop()

print("Completed processing")

