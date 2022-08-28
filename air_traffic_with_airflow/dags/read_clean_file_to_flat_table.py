from datetime import datetime, timedelta
import os

from opensky_api_master.python.opensky_api import OpenSkyApi
from constant_values import api_login_data
from packages import modules

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.operators.bash import BashOperator

default_args = {
    'owner': 'wjudt',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}

# def read_file_from_clean_bucket(ts_nodash, bucket_name: str, local_path: str) -> str:
#     s3_hook = S3Hook(aws_conn_id="minio_connection")
#     old_file_path = s3_hook.download_file(
#         bucket_name=bucket_name,
#         key=f"zone1_{ts_nodash}.csv",
#         local_path=local_path
#     )
#     old_file_name = old_file_path.split('/')[-1]
#     downloaded_file_path = f"./download/{old_file_name}"
#     new_file_path = f"./download/zone1_{ts_nodash}.csv"
#     os.rename(src=downloaded_file_path, dst=new_file_path)
#     return new_file_path


with DAG(
        default_args=default_args,
        dag_id='read_clean_data',
        description='Dag for retrieving data from open sky api',
        start_date=datetime(2022, 8, 22),
        schedule_interval='*/15 * * * *',
        catchup=False,
        tags=['open_sky']
) as dag:
    # task1 = PythonOperator(
    #     task_id='read_file_from_clean_bucket',
    #     python_callable=read_file_from_clean_bucket,
    #     op_kwargs={
    #         "bucket_name": "open-sky-clean-data",
    #         "local_path": r"/opt/airflow/download/"
    #     }
    #     )

    task2 = PostgresOperator(
        task_id='create_db_table',
        postgres_conn_id='postgres_connection',
        sql='sql_queries/create_flat_table.sql'

    )

    task3 = PostgresOperator(
        task_id='delete_duplicates',
        postgres_conn_id='postgres_connection',
        sql="""
        delete from area1_flat 
        where dag_utc_time_str = TIMESTAMP'2022-08-28 12:30:00.000';
        """
    )

    task4 = PostgresOperator(
        task_id='insert_data_to_db',
        postgres_conn_id='postgres_connection',
        sql="""
        copy area1_flat
        from '/insert_data/zone1_20220828T123000_clean.csv'
        delimiter ',' csv;
        """
    )

    task2 >> task3 >> task4