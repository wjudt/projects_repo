from datetime import datetime, timedelta
import os
import shutil

from opensky_api_master.python.opensky_api import OpenSkyApi
from constant_values import api_login_data
from packages import modules

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

default_args = {
    'owner': 'wjudt',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


def get_api_data_sent_to_minio(username: str, password: str, ts_nodash) -> None:
    api = OpenSkyApi(username=username, password=password)
    response = api.get_states(bbox=(51, 53, 16, 18))
    data = str(response)

    s3_hook = S3Hook(aws_conn_id="minio_connection")
    s3_hook.load_string(
        string_data=data,
        key=f"zone1_{ts_nodash}.csv",
        bucket_name="open-sky-raw-data",
        replace=True
    )
    print(f'data properly saved to a file: zone1_{ts_nodash}.csv')


def read_file_from_raw_bucket(ts_nodash, bucket_name: str, local_path: str) -> str:
    s3_hook = S3Hook(aws_conn_id="minio_connection")
    old_file_path = s3_hook.download_file(
        bucket_name=bucket_name,
        key=f"zone1_{ts_nodash}.csv",
        local_path=local_path
    )
    old_file_name = old_file_path.split('/')[-1]
    downloaded_file_path = f"./download/{old_file_name}"
    new_file_path = f"./download/zone1_{ts_nodash}.csv"
    os.rename(src=downloaded_file_path, dst=new_file_path)
    return new_file_path


def clean_data_save_to_local_file(ti, ts_nodash, execution_date, ts) -> str:
    file_path = ti.xcom_pull(task_ids=["read_file_from_raw_bucket"])
    print(file_path)
    date = ts
    print(type(date))
    df = modules.clean_data(path=file_path[0], execution_date=date)
    clean_csv_path = f"./download/zone1_{ts_nodash}_clean.csv"
    df.to_csv(clean_csv_path, index=False, header=False)
    print(f'data properly saved to a file: {clean_csv_path}')
    return clean_csv_path


def upload_local_file_to_clean_bucket(ti, ts_nodash):
    csv_new_path = ti.xcom_pull(task_ids='clean_data_save_to_local_file')
    csv_old_path = ti.xcom_pull(task_ids='read_file_from_raw_bucket')
    s3_hook = S3Hook(aws_conn_id="minio_connection")
    s3_hook.load_file(
        filename=csv_new_path,
        key=f"zone1_{ts_nodash}_clean.csv",
        bucket_name="open-sky-clean-data",
        replace=True
    )
    os.remove(csv_new_path)
    os.remove(csv_old_path)


def read_file_from_clean_bucket(ts_nodash, bucket_name: str, local_path: str) -> str:
    s3_hook = S3Hook(aws_conn_id="minio_connection")
    old_file_path = s3_hook.download_file(
        bucket_name=bucket_name,
        key=f"zone1_{ts_nodash}_clean.csv",
        local_path=local_path
    )
    old_file_name = old_file_path.split('/')[-1]
    downloaded_file_path = f"./download/{old_file_name}"
    new_file_path = f"./postgres/insert_data/zone1_{ts_nodash}_clean.csv"
    shutil.move(src=downloaded_file_path, dst=new_file_path)
    print(f"file path: {new_file_path}")
    cut_file_path = new_file_path.split('/')[-1]
    print(f"cut file path: {cut_file_path}")
    return cut_file_path


with DAG(
        default_args=default_args,
        dag_id='open_sky_api_v8',
        description='Dag for retrieving data from open sky api',
        start_date=datetime(2022, 8, 22),
        schedule_interval='*/15 * * * *',
        catchup=False,
        tags=['open_sky']
) as dag:
    task1 = PythonOperator(
        task_id='get_api_data',
        python_callable=get_api_data_sent_to_minio,
        op_kwargs={'username': api_login_data.api_username,
                   'password': api_login_data.api_password}
    )

    task2 = PythonOperator(
        task_id='read_file_from_raw_bucket',
        python_callable=read_file_from_raw_bucket,
        op_kwargs={
            "bucket_name": "open-sky-raw-data",
            "local_path": r"/opt/airflow/download/"
        }
    )

    task3 = PythonOperator(
        task_id='clean_data_save_to_local_file',
        python_callable=clean_data_save_to_local_file
    )

    task4 = PythonOperator(
        task_id='upload_local_file_to_clean_bucket',
        python_callable=upload_local_file_to_clean_bucket,
    )

    task5 = PythonOperator(
        task_id='read_file_from_clean_bucket',
        python_callable=read_file_from_clean_bucket,
        op_kwargs={
            "bucket_name": "open-sky-clean-data",
            "local_path": r"/opt/airflow/download/"
        }
    )

    task6 = PostgresOperator(
        task_id='create_db_table',
        postgres_conn_id='postgres_connection',
        sql='sql_queries/create_flat_table.sql'
    )

    task7 = PostgresOperator(
        task_id='delete_duplicates',
        postgres_conn_id='postgres_connection',
        sql="""
        delete from area1_flat 
        where dag_utc_time_str = TIMESTAMP'{{ ts_nodash }}';
        """
    )

    task8 = PostgresOperator(
        task_id='insert_data_to_db',
        postgres_conn_id='postgres_connection',
        sql="""
        copy area1_flat
        from '/insert_data/{{ti.xcom_pull(task_ids='read_file_from_clean_bucket')}}'
        delimiter ',' csv;
        """
    )

    task1 >> task2 >> task3 >> task4 >> task5 >> task6 >> task7 >> task8
