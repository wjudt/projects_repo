from datetime import datetime, timedelta
import os

from opensky_api_master.python.opensky_api import OpenSkyApi
from constant_values import api_login_data
from packages import modules

from airflow import DAG
from airflow.operators.python import PythonOperator
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


def read_file_from_minio(ts_nodash, bucket_name: str, local_path: str) -> str:
    s3_hook = S3Hook(aws_conn_id="minio_connection")
    file_name = s3_hook.download_file(
        bucket_name=bucket_name,
        key=f"zone1_{ts_nodash}.csv",
        local_path=local_path
    )
    return file_name


def rename_file_from_minio(ti, ts_nodash) -> str:
    previous_file_path = ti.xcom_pull(task_ids=["download_file_from_minio"])
    previous_file_name = previous_file_path[0].split('/')[-1]
    downloaded_file_path = f"./download/{previous_file_name}"
    new_file_path = f"./download/zone1_{ts_nodash}.csv"
    os.rename(src=downloaded_file_path, dst=new_file_path)
    return new_file_path


def clean_data_save_to_parquet(ti, ts_nodash) -> str:
    file_path = ti.xcom_pull(task_ids=["rename_file_from_minio"])
    print(file_path)
    df = modules.clean_data(file_path[0])
    parquet_path = f"./download/zone1_{ts_nodash}.parquet"
    df.to_parquet(parquet_path)
    print(f'data properly saved to a file: {parquet_path}')
    return parquet_path


def upload_parquet_to_minio(ti, ts_nodash):
    parquet_path = ti.xcom_pull(task_ids='clean_data_save_to_parquet')
    csv_path = ti.xcom_pull(task_ids='rename_file_from_minio')
    s3_hook = S3Hook(aws_conn_id="minio_connection")
    s3_hook.load_file(
        filename=parquet_path,
        key=f"zone1_{ts_nodash}.parquet",
        bucket_name="open-sky-clean-data",
        replace=True
    )
    os.remove(parquet_path)
    os.remove(csv_path)



with DAG(
        default_args=default_args,
        dag_id='open_sky_api_v6',
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
        task_id='download_file_from_minio',
        python_callable=read_file_from_minio,
        op_kwargs={
            "bucket_name": "open-sky-raw-data",
            "local_path": r"/opt/airflow/download/"
        }
        )

    task3 = PythonOperator(
        task_id='rename_file_from_minio',
        python_callable=rename_file_from_minio
        )

    task4 = PythonOperator(
        task_id='clean_data_save_to_parquet',
        python_callable=clean_data_save_to_parquet
        )

    task5 = PythonOperator(
        task_id='upload_parquet_to_minio',
        python_callable=upload_parquet_to_minio,
        )

    task1 >> task2 >> task3 >> task4 >> task5

