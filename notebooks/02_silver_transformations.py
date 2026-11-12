# Fabric notebook: 02_silver_transformations
from pyspark.sql import functions as F

# Latest customer snapshot is batch 2. SCD history is handled separately in notebook 03.
customers = (spark.table("bronze.bronze_customers_batch2")
    .select("customer_id", "customer_name", "city", "state",
            F.to_timestamp("updated_at").alias("source_updated_at"))
    .dropDuplicates(["customer_id"]))

orders = (spark.table("bronze.bronze_orders")
    .select("order_id", "customer_id", F.to_date("order_date").alias("order_date"),
            F.trim("order_status").alias("order_status"))
    .dropDuplicates(["order_id"]))

items = (spark.table("bronze.bronze_order_items")
    .select("order_id", "product_id", F.col("quantity").cast("int"),
            F.col("unit_price").cast("decimal(12,2)"))
    .filter((F.col("quantity") > 0) & (F.col("unit_price") >= 0)))

products = (spark.table("bronze.bronze_products")
    .select("product_id", F.trim("product_name").alias("product_name"),
            F.trim("category").alias("category"))
    .dropDuplicates(["product_id"]))

for df, name in [(customers,"silver_customers"),(orders,"silver_orders"),
                 (items,"silver_order_items"),(products,"silver_products")]:
    df.write.format("delta").mode("overwrite").option("overwriteSchema","true").saveAsTable(f"silver.{name}")
    print(name, df.count())
