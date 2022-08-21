from airflow import DAG
from datetime import datetime, timedelta
from airflow.operators.python import PythonOperator
from opensky_api_master.python.opensky_api import OpenSkyApi
from constant_values import api_login_data

default_args = {
    'owner': 'wjudt',
    'retries': 3,
    'retry_delay': timedelta(minutes=5)
}


def get_api_data(username, password):
    api = OpenSkyApi(username=username, password=password)
    s = api.get_states(bbox=(51, 53, 16, 18))
    print(s)


with DAG(
        default_args=default_args,
        dag_id='open_sky_api',
        description='Dag for retrieving data from open sky api',
        start_date=datetime(2022, 8, 20),
        schedule_interval='*/15 * * * *',
        catchup=False,
        tags=['open_sky']
) as dag:
    task1 = PythonOperator(
        task_id='get_api_data_sent_raw_to_minio',
        python_callable=get_api_data,
        op_kwargs={'username': api_login_data.api_username,
                   'password': api_login_data.api_password}
    )
