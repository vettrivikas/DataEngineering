from pyspark.sql import SparkSession
from pyspark.sql.functions import lit

appName = "PySpark Hive Example"
master = "local"

# Create Spark session with Hive supported.
spark = SparkSession.builder \
    .appName(appName) \
    .master(master) \
    .enableHiveSupport() \
    .getOrCreate()

# Read data from Hive database test_db, table name: test_table.
df = spark.sql("select * from test_db.test_table")
df.show()

# Let's add a new column
df = df.withColumn("NewColumn",lit('Test'))
df.show()

# Save df to a new table in Hive
df.write.mode("overwrite").saveAsTable("test_db.test_table2")
# Show the results using SELECT
spark.sql("select * from test_db.test_table2").show()

# Append data via SQL
spark.sql("insert into test_db.test_table2 values (3, 'GHI', 'SQL INSERT')")
spark.sql("select * from test_db.test_table2").show()

# Append data via code
df = spark.sql("select 4 as id, 'JKL' as value, 'Spark Write Append Mode' as NewColumn")
df.show()
df.write.mode("append").saveAsTable("test_db.test_table2")
spark.sql("select * from test_db.test_table2").show()
