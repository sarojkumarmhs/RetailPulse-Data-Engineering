# Fabric notebook: 01_bronze_ingestion
from pyspark.sql import functions as F

# Fabric default Lakehouse paths are relative to the Lakehouse Files area.
SOURCE_ROOT = "Files/source"

def ingest_csv(path, table_name):
    df = (spark.read.option("header", True)
          .option("inferSchema", True)
          .csv(path)
          .withColumn("_ingested_at", F.current_timestamp())
          .withColumn("_source_file", F.input_file_name()))
    if df.limit(1).count() == 0:
        raise ValueError(f"No rows found at {path}")
    (df.write.format("delta").mode("overwrite").option("overwriteSchema", "true")
       .saveAsTable(f"bronze.{table_name}"))
    print(f"{table_name}: {df.count()} rows")
    return df

ingest_csv(f"{SOURCE_ROOT}/customers/batch_1/customers.csv", "bronze_customers_batch1")
ingest_csv(f"{SOURCE_ROOT}/customers/batch_2/customers.csv", "bronze_customers_batch2")
ingest_csv(f"{SOURCE_ROOT}/orders/batch_1/orders.csv", "bronze_orders")
ingest_csv(f"{SOURCE_ROOT}/order_items/batch_1/order_items.csv", "bronze_order_items")
ingest_csv(f"{SOURCE_ROOT}/products/products.csv", "bronze_products")
