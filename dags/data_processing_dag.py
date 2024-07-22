from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}
def run_spark_job():
    from pyspark.sql.functions import concat_ws, count, collect_list
    from pyspark.sql import SparkSession

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


    person_df = spark.read.csv("s3a://data/person_data.csv", header=True)

    country_df = spark.read.csv("s3a://data/"
                                "", header=True)

    result_df = (person_df
                 .where((person_df.birthday < datetime.now() - relativedelta(years=30)) & (person_df.blood_type.isin('A+', 'A-', 'AB+', 'AB-')))
                 .groupBy(person_df.country)
                 .agg(count('*').alias('count'), concat_ws(', ', collect_list('first_name')).alias('names'))
                 .join(country_df, person_df.country == country_df.country, 'left')
                 .select('country_name', 'count', 'names'))

    result_df.write.mode("overwrite").csv('s3a://data/output.csv', header=True)

    spark.stop()


with DAG('data_processing_dag',
         start_date=datetime(2024, 7, 16),
         schedule=timedelta(minutes=10),
         catchup=False) as dag:
    spark_task = PythonOperator(
        task_id='run_spark_job',
        python_callable=run_spark_job
    )

start = EmptyOperator(task_id="start", dag=dag)


end = EmptyOperator(task_id="end", dag=dag)


start >> spark_task >> end

