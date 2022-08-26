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


def clean_data_save_to_local_file(ti, ts_nodash, execution_date) -> str:
    file_path = ti.xcom_pull(task_ids=["read_file_from_raw_bucket"])
    print(file_path)
    df = modules.clean_data(path=file_path[0], execution_date=execution_date)
    clean_csv_path = f"./download/zone1_{ts_nodash}_clean.csv"
    df.to_csv(clean_csv_path, index=False)
    print(f'data properly saved to a file: {clean_csv_path}')
    return clean_csv_path


def upload_clean_data_to_minio(ti, ts_nodash):
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


with DAG(
        default_args=default_args,
        dag_id='open_sky_api_v7',
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
        task_id='upload_clean_data_to_minio',
        python_callable=upload_clean_data_to_minio,
    )

    task1 >> task2 >> task3 >> task4
