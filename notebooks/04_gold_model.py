# Fabric notebook: 04_gold_model
from pyspark.sql import functions as F
from pyspark.sql.window import Window

# Product dimension
products = spark.table("silver.silver_products")
(products.withColumn("product_key", F.xxhash64("product_id"))
 .select("product_key","product_id","product_name","category")
 .write.format("delta").mode("overwrite").option("overwriteSchema","true")
 .saveAsTable("gold.dim_product"))

# Order fact: one row per order line. Resolve the customer to the current dimension key via business key.
orders = spark.table("silver.silver_orders").alias("o")
items = spark.table("silver.silver_order_items").alias("i")
customers = (spark.table("gold.dim_customer").filter("is_current = true")
             .select("customer_id","customer_key")).alias("c")
products_key = spark.table("gold.dim_product").select("product_id","product_key").alias("p")

fact = (orders.join(items,"order_id")
    .join(customers, "customer_id", "left")
    .join(products_key, "product_id", "left")
    .withColumn("gross_amount", (F.col("quantity")*F.col("unit_price")).cast("decimal(14,2)"))
    .select("order_id","customer_id","customer_key","product_id","product_key",
            "order_date","order_status","quantity","unit_price","gross_amount"))

(fact.write.format("delta").mode("overwrite").option("overwriteSchema","true")
 .saveAsTable("gold.fact_order"))

display(spark.table("gold.fact_order"))
