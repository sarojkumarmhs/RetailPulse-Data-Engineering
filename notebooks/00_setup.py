# Fabric notebook: 00_setup
# Attach RetailPulseLH as the default Lakehouse before running.
from pyspark.sql import functions as F
from pyspark.sql import types as T

spark.sql("CREATE SCHEMA IF NOT EXISTS bronze")
spark.sql("CREATE SCHEMA IF NOT EXISTS silver")
spark.sql("CREATE SCHEMA IF NOT EXISTS gold")
spark.sql("CREATE SCHEMA IF NOT EXISTS audit")

print("RetailPulse schemas are ready.")
