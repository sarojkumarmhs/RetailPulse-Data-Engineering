# Fabric notebook: 05_data_quality
from pyspark.sql import functions as F
from datetime import datetime

checks = []
def record(check_name, failed_count, severity="ERROR"):
    checks.append((check_name, int(failed_count), severity, datetime.utcnow()))

orders = spark.table("silver.silver_orders")
items = spark.table("silver.silver_order_items")
customers = spark.table("gold.dim_customer")
fact = spark.table("gold.fact_order")

record("orders_order_id_not_null", orders.filter(F.col("order_id").isNull()).count())
record("orders_customer_id_not_null", orders.filter(F.col("customer_id").isNull()).count())
record("order_items_positive_quantity", items.filter(F.col("quantity").isNull() | (F.col("quantity") <= 0)).count())
record("order_items_non_negative_price", items.filter(F.col("unit_price").isNull() | (F.col("unit_price") < 0)).count())
record("dim_customer_one_current_per_business_key",
       customers.filter("is_current = true").groupBy("customer_id").count().filter("count != 1").count())
record("fact_order_missing_customer_key", fact.filter(F.col("customer_key").isNull()).count())

schema = "check_name string, failed_count long, severity string, checked_at timestamp"
results = spark.createDataFrame(checks, schema=schema)
results = results.withColumn("status", F.when(F.col("failed_count")==0,"PASS").otherwise("FAIL"))
(results.write.format("delta").mode("overwrite").option("overwriteSchema","true")
 .saveAsTable("audit.dq_results"))
display(results.orderBy("status","check_name"))

failed = results.filter("status = 'FAIL'").count()
if failed:
    raise Exception(f"RetailPulse data quality failed: {failed} check(s)")
print("All data quality checks passed.")
