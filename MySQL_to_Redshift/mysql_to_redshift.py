from pyspark.sql.types import *
from pyspark.sql import SparkSession
from pyspark.sql.functions import *
import sys
import ast

if sys.platform.startswith('linux'):
    sys.path.append("configpath")
    sys.path.append("configpath")

elif sys.platform.startswith('win'):
    sys.path.append(r"path")

from config import servers,aws_access_key_id,aws_secret_access_key,to_addr, cc_addr
from MailUtils import sendmail



class generic_code:
    def __init__(self):
        try:
            self.spark = SparkSession.builder \
                .appName('myAppName') \
                .master("local[*]") \
                .config("spark.driver.extraClassPath",
                        "/path/RedshiftJDBC42-1.2.43.1067.jar") \
                .config("spark.jars.packages", "com.amazonaws:aws-java-sdk:1.7.4") \
                .getOrCreate()
            self.tempREDSHIFT_JDBC_URL = "redshifturl"
        except Exception as exe:
            print(exe)

    def get_connection(self, host_name, db_name, table_list, taget_db):
        try:
            if host_name == "hostname" or host_name == "hostname2" or host_name == "hostname2":
            print(host_name)
                for i in table_list:
                    query1 = "select * from " + db_name + "." + i
                    query = "(" + query1 + ") data"
                    tabel_name = taget_db+"." + i.lower()
                    j = self.spark.read.format("jdbc").option("url", "jdbc:mysql://" + host_name + ":3306") \
                        .option("driver", "com.mysql.jdbc.Driver").option("dbtable", query) \
                        .option("user", servers[host_name].get('username')).option("password", servers[host_name].get('password')).load()
                    j.show(10)
                    j.write \
                        .format("io.github.spark_redshift_community.spark.redshift") \
                        .option("url", self.tempREDSHIFT_JDBC_URL) \
                        .option("forward_spark_s3_credentials", "true") \
                        .option("dbtable", tabel_name) \
                        .option("aws_region", "us-west-2") \
                        .option("tempdir",
                                "s3a://" + aws_access_key_id + ":" + aws_secret_access_key + "@s3location") \
                        .mode("append") \
                        .save()
                    j.show()
        except Exception as exe:
            email_subject = "MySQL_to_Redshift error: "
            email_content = "Error: [MySQL to redshift]- Exception while coping mysql to redshift:" + str(exe)
            sendmail(email_subject, email_content, [], to_addr, cc_addr)
            print(email_content)
            
if __name__ == "__main__":
    oc = generic_code()
    def Convert(string):
        li = list(string.split(","))
        return li
    host_name = sys.argv[1]
    db_name = sys.argv[2]
    tables = sys.argv[3]
    taget_db = sys.argv[4]
    table_list = Convert(tables)
    oc.get_connection(host_name, db_name, table_list, taget_db)
    #spark-submit /mysql2red.py 'host_name' 'dbname' "table1,table12,table13" "target_db"






