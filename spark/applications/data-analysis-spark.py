from pyspark.sql.functions import concat_ws, count, collect_list
from pyspark.sql import SparkSession
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

def readAndProcessData():

    # Create Spark session
    spark = (SparkSession.builder
             .appName("DataAnalysisSpark")
             .master("local")
             .config("spark.hadoop.fs.s3a.access.key", "minioadmin")
             .config("spark.hadoop.fs.s3a.secret.key", "minioadmin")
             .config("spark.hadoop.fs.s3a.endpoint", "http://minio-server:9000")
             .config("spark.hadoop.fs.s3a.path.style.access", "true")
             .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
             .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false")
             .config("spark.driver.extraJavaOptions", "--add-exports java.base/sun.nio.ch=ALL-UNNAMED")
             .getOrCreate())

    log4jLogger = spark._jvm.org.apache.log4j
    LOGGER = log4jLogger.LogManager.getLogger(__name__)

    person_df = spark.read.csv("s3a://data/person_data.csv", header=True)

    country_df = spark.read.csv("s3a://data/country_data.csv", header=True)


    LOGGER.info("Data Successfully Read *****************************************")

    result_df = (person_df
                 .where((person_df.birthday < datetime.now() - relativedelta(years=30)) & (person_df.blood_type.isin('A+', 'A-', 'AB+', 'AB-')))
                 .groupBy(person_df.country)
                 .agg(count('*').alias('count'), concat_ws(', ', collect_list('first_name')).alias('names'))
                 .join(country_df, person_df.country == country_df.country, 'left')
                 .select('country_name', 'count', 'names'))

    result_df.write.mode("overwrite").csv('s3a://data/output.csv', header=True)
    LOGGER.info("Data Successfully Written ****************************************")

    spark.stop()
