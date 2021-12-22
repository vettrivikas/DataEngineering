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

query = "('select * from testdb.test_table limit 10') data"
df = spark.read.format("jdbc").option("url", "jdbc:mysql://localhost:3306") \
     .option("driver", "com.mysql.jdbc.Driver").option("dbtable", query) \
     .option("user", 'user_name').option("password", 'pass').load()
df.show(10)

# Read data from Hive database test_db, table name: test_table.
#df = spark.sql("select * from test_db.test_table")
#df.show()

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







-----------------------------------------------------------------------------



def save_table(sparkSession, dataframe, database, table_name, save_format="PARQUET"):
    print("Saving result in {}.{}".format(database, table_name))
    output_schema = "," \
        .join(["{} {}".format(x.name.lower(), x.dataType) for x in list(dataframe.schema)]) \
        .replace("StringType", "STRING") \
        .replace("IntegerType", "INT") \
        .replace("DateType", "DATE") \
        .replace("LongType", "INT") \
        .replace("TimestampType", "INT") \
        .replace("BooleanType", "BOOLEAN") \
        .replace("FloatType", "FLOAT")\
        .replace("DoubleType","FLOAT")
    output_schema = re.sub(r'DecimalType[(][0-9]+,[0-9]+[)]', 'FLOAT', output_schema)

    sparkSession.sql("DROP TABLE IF EXISTS {}.{}".format(database, table_name))

    query = "CREATE EXTERNAL TABLE IF NOT EXISTS {}.{} ({}) STORED AS {} LOCATION '/user/hive/{}/{}'" \
        .format(database, table_name, output_schema, save_format, database, table_name)
    sparkSession.sql(query)
    dataframe.write.insertInto('{}.{}'.format(database, table_name),overwrite = True)
