# Fabric notebook: 03_customer_scd_type2
from pyspark.sql import functions as F
from delta.tables import DeltaTable

# Use batch 1 as the initial dimension snapshot, then apply batch 2 as the incoming snapshot.
initial = (spark.table("bronze.bronze_customers_batch1")
    .select("customer_id","customer_name","city","state",
            F.to_timestamp("updated_at").alias("source_updated_at"))
    .withColumn("effective_from", F.to_timestamp("source_updated_at"))
    .withColumn("customer_key", F.xxhash64("customer_id", F.to_timestamp("source_updated_at")))
    .withColumn("effective_to", F.lit(None).cast("timestamp"))
    .withColumn("is_current", F.lit(True))
    .withColumn("attribute_hash", F.sha2(F.concat_ws("||","customer_name","city","state"),256)))

(initial.write.format("delta").mode("overwrite").option("overwriteSchema","true")
 .saveAsTable("gold.dim_customer"))

incoming = (spark.table("bronze.bronze_customers_batch2")
    .select("customer_id","customer_name","city","state",
            F.to_timestamp("updated_at").alias("source_updated_at"))
    .withColumn("attribute_hash", F.sha2(F.concat_ws("||","customer_name","city","state"),256))
    .dropDuplicates(["customer_id"]))

dim = DeltaTable.forName(spark, "gold.dim_customer")
current = spark.table("gold.dim_customer").filter("is_current = true").select("customer_id","attribute_hash")
changed = (incoming.alias("s").join(current.alias("t"),"customer_id","inner")
           .filter(F.col("s.attribute_hash") != F.col("t.attribute_hash"))
           .select("s.*"))

# Expire changed current records.
if changed.limit(1).count() > 0:
    (dim.alias("t").merge(changed.alias("s"), "t.customer_id = s.customer_id AND t.is_current = true")
     .whenMatchedUpdate(set={"effective_to":"s.source_updated_at", "is_current":"false"})
     .execute())

# Insert new customers and changed versions. Unchanged customers are not reinserted.
current_after = spark.table("gold.dim_customer").filter("is_current = true").select("customer_id","attribute_hash")
to_insert = (incoming.alias("s").join(current_after.alias("t"),"customer_id","left")
             .filter(F.col("t.customer_id").isNull())
             .select("s.customer_id","s.customer_name","s.city","s.state","s.source_updated_at","s.attribute_hash")
             .withColumn("effective_from",F.col("source_updated_at"))
             .withColumn("customer_key",F.xxhash64("customer_id",F.col("source_updated_at")))
             .withColumn("effective_to",F.lit(None).cast("timestamp"))
             .withColumn("is_current",F.lit(True)))
to_insert.write.format("delta").mode("append").saveAsTable("gold.dim_customer")

print("SCD2 current rows:", spark.table("gold.dim_customer").filter("is_current = true").count())
display(spark.table("gold.dim_customer").orderBy("customer_id","effective_from"))
