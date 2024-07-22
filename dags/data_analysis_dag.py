import os
from airflow import DAG
from airflow.operators.empty import EmptyOperator
from datetime import datetime, timedelta
from airflow.contrib.operators.spark_submit_operator import SparkSubmitOperator

###############################################
# Parameters
###############################################
spark_conn = os.environ.get("spark_conn", "spark_conn")
spark_master = "spark://spark:7077"
spark_app_name = "Spark Data Analysis"

###############################################
# DAG Definition
###############################################
now = datetime.now()


default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "start_date": datetime(now.year, now.month, now.day),
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=1)
}

dag = DAG(
    dag_id="data-analysis-test",
    description="This DAG runs a data analysis Pyspark app.",
    default_args=default_args,
    schedule_interval=timedelta(minutes=10)
)


start = EmptyOperator(task_id="start", dag=dag)

spark_job2 = SparkSubmitOperator(
    task_id="spark_job2",
    # Spark application path created in airflow and spark cluster
    application="/opt/airflow/spark/applications/data-analysis-spark.py",
    name=spark_app_name,
    conn_id=spark_conn,
    verbose=1,
    conf={"spark.master": spark_master},
    # application_args=[file_path],
    dag=dag)

end = EmptyOperator(task_id="end", dag=dag)


start >> spark_job2 >> end
