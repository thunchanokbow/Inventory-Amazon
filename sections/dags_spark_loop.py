
"""
How to automate spark job in Dataproc with Apache Airflow in GCC
1. Create the dataset in Google BigQuery
2. Create the storage in GCS and Upload files "sales_report.csv" AND "pyspark_demo_NEW.py" (BUCKET ONE)
3. Create the cluster in Dataproc and config same bucket in GCS using shell scripts
4. Create the GCC to connect with Airflow (BUCKET TWO)
5. Upload DAG file to BUCKET TWO using Cloud shell

Airflow operators for managing a dataproc cluster 
    1. Create Dataproc cluster
    2. Submit PySpark jobs (in parallel)
    3. Upload Spark Output files to BigQuery 
    4. Delete dataproc cluster
"""

import os
from datetime import datetime
import pandas as pd
from airflow import models
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.operators.gcs import GCSDeleteObjectsOperator 
from airflow.providers.google.cloud.transfers.postgres_to_gcs import PostgresToGCSOperator 
from airflow.providers.google.cloud.operators.dataproc import (
    ClusterGenerator,
    DataprocCreateClusterOperator,
    DataprocDeleteClusterOperator,
    DataprocSubmitJobOperator
)


# Google Cloud Storage
GCS_BUCKET = 'dataproc-spark-demo'
GCS_OBJECT_PATH = 'postgresql'
HIGH_REPORT_OUTPUT = 'gs://dataproc-spark-demo/postgresql/high_report.csv'
Table_names = ["monthly_sales", "best_revenue", "Inventory_Value"]
# PostgreSQL Config
TABLE_NAMES = ["sales_report", "product_price"]
HIGH_TABLE_NAME = 'high_report'
DELETE_TABLE = ["sales_report", "product_price", "high_report"]
POSTGRESS_CONNECTION_ID = 'postgres_default'
FILE_FORMAT = 'csv'
# This one will connect to DAG in Airflow
DAG_ID = "dataproc_cluster_jobs" 
# Project ID not NAME of the project 
PROJECT_ID = "best-seller-amazon"
# Pyspark Job AND Dataproc Cluster Bucket
# BUCKET_NAME = "dataproc-spark-demo"
# Dataproc cluster Config
CLUSTER_NAME = "spark-dataproc"
REGION = "asia-east2"
ZONE = "asia-east2-b"
# PysPark Job Config
SCRIPT_BUCKET_PATH = "dataproc-spark-demo/scripts"
# GCS -> AGGREGATE -> BQ
SCRIPT_NAME = "final-spark.py"


# Cluster definition: Generating Cluster Config for DataprocCreateClusterOperator
INIT_FILE = "goog-dataproc-initialization-actions-asia-east2/connectors/connectors.sh"

# Generating cluster Configurations with this operator
CLUSTER_GENERATOR_CONFIG = ClusterGenerator(
    project_id=PROJECT_ID,
    zone=ZONE,
    master_machine_type="n1-standard-2",
    worker_machine_type="n1-standard-2",
    num_workers=2,
    storage_bucket=GCS_BUCKET,
    init_actions_uris=[f"gs://{INIT_FILE}"],
    metadata={"bigquery-connector-version":"1.2.0","spark-bigquery-connector-version":"0.21.0"}
).make()


# Spark job configs 
PYSPARK_DEMO =  { 
                "reference": {"project_id": PROJECT_ID},
                "placement": {"cluster_name": CLUSTER_NAME},
                "pyspark_job": {"main_python_file_uri": f"gs://{SCRIPT_BUCKET_PATH}/{SCRIPT_NAME}"},
                } 

# Pandas job  
def get_data_from_bucket(high_report): 
    # Read Pandas Dataframe.
    high_report_pd = pd.read_csv('gs://dataproc-spark-demo/postgresql/sales_report.csv')
    # Convert the Date column to a datetime dtype New_date column.
    high_report_pd["New_date"] = pd.to_datetime(high_report_pd["date"])
    # Save this file in postgresql bucket
    high_report_pd.to_csv(high_report, header=True)



# DAG definition is here
with models.DAG(
    DAG_ID,
    schedule="@once",
    start_date=datetime(2023, 9, 13), 
    catchup=False,
    tags=["example", "dataproc"],
) as dag:
    


    # Create cluster with generates cluster config operator
    create_dataproc_cluster = DataprocCreateClusterOperator(
        task_id="create_dataproc_cluster",
        cluster_name=CLUSTER_NAME,
        project_id=PROJECT_ID,
        region=REGION,
        cluster_config=CLUSTER_GENERATOR_CONFIG,
    )

    postgres_to_gcs = []
    # Postgres connection
    for table_name in TABLE_NAMES:
        postgres_to_gcs.append(
            PostgresToGCSOperator(
                task_id=f'postgres_to_gcs_{table_name}',
                postgres_conn_id=POSTGRESS_CONNECTION_ID,
                sql=f'SELECT * FROM {table_name};',
                bucket=GCS_BUCKET,
                filename=f'{GCS_OBJECT_PATH}/{table_name}.{FILE_FORMAT}',
                export_format='csv',
                gzip=False,
                use_server_side_cursor=False,
            )
        )
    for i in range(len(postgres_to_gcs) - 1):
        postgres_to_gcs[i] >> postgres_to_gcs[i + 1]    

    # Pandas task 
    pandas_task = PythonOperator(
        task_id="get_data_from_bucket",
        python_callable=get_data_from_bucket,
        op_kwargs={"high_report": HIGH_REPORT_OUTPUT},
    )
    # Set task dependencies
    [create_dataproc_cluster, postgres_to_gcs[-1]] >> pandas_task


    # PySpark task to read data from GCS , perform agrregate on data and write data into Bigquery
    pyspark_task_demo = DataprocSubmitJobOperator(
        task_id="pyspark_task_demo", 
        job=PYSPARK_DEMO, 
        region=REGION, 
        project_id=PROJECT_ID,
    )
    # Set task dependencies
    pandas_task >> pyspark_task_demo

    storage_bigQuery = []
    # Upload output spark files to BigQuery
    for Table_name in Table_names:
        storage_bigQuery.append(
            BashOperator(
                task_id=f"storage_bigQuery_{Table_name}",                                 
                bash_command=f"bq load \
                    --source_format=CSV \
                    --autodetect \
                    dataproc_spark.{Table_name} \
                    gs://dataproc-spark-demo/jobs/{Table_name}/*.csv"
            )                
        )

    for i in range(len(storage_bigQuery) - 1):
        storage_bigQuery[i] >> storage_bigQuery[i + 1]     
     # Set task dependencies
    pyspark_task_demo >> storage_bigQuery[0]          

    # Delete Cluster once done with jobs
    delete_cluster = DataprocDeleteClusterOperator(
        task_id="delete_cluster",
        project_id=PROJECT_ID,
        cluster_name=CLUSTER_NAME,
        region=REGION
    )
    # Set task dependencies
    pyspark_task_demo >> delete_cluster    

    delete_postgres_sales = []
    # Delete files from postgresql bucket
    for files in DELETE_TABLE:
        delete_postgres_sales.append(
            GCSDeleteObjectsOperator(
                task_id=f'delete_postgres_sales_{files}',
                bucket_name=GCS_BUCKET,
                objects=[f'{GCS_OBJECT_PATH}/{files}.csv'],
            )
        )
    
    for i in range(len(delete_postgres_sales)- 1):
        delete_postgres_sales[i] >> delete_postgres_sales[i + 1]
    # Set task dependencies
    pyspark_task_demo >> delete_postgres_sales[0]
