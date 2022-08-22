from datetime import datetime, timedelta

from opensky_api_master.python.opensky_api import OpenSkyApi
from constant_values import api_login_data

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook


default_args = {
    'owner': 'wjudt',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


def get_api_data_sent_to_minio(username, password, ts_nodash):
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

    print(data)
    print(type(data))


with DAG(
        default_args=default_args,
        dag_id='open_sky_api',
        description='Dag for retrieving data from open sky api',
        start_date=datetime(2022, 8, 22),
        schedule_interval='*/15 * * * *',
        catchup=False,
        tags=['open_sky']
) as dag:
    task1 = PythonOperator(
        task_id='get_api_data_sent_raw_to_minio',
        python_callable=get_api_data_sent_to_minio,
        op_kwargs={'username': api_login_data.api_username,
                   'password': api_login_data.api_password}
    )
