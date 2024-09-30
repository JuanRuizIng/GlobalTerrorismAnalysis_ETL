# Libraries to work with Airflow
# --------------------------------

from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Importing the necessary modules and env variables
# --------------------------------

from tasks.etl import *

default_args = {
    'owner': "airflow",
    'depends_on_past': False,
    'start_date': datetime(2024, 8, 14),
    'email': "example@example.com",
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=120)
}

@dag(
    default_args=default_args,
    description='Creating an ETL pipeline for our GTA database.',
    schedule=timedelta(days=1),
    max_active_runs=1,
    catchup=False,
    concurrency=4,
)

def gta_dag():
    """
    This DAG is going to execute the ETL pipeline for the Global Terrorism Analysis project.
    
    """
    @task
    def extract_raw_db_task():
        return extract_raw_db()
    
    @task
    def extract_api_task():
        return extract_api()
    
    @task
    def transform_db_task(df_json):
        return transform_db(df_json)
    
    @task
    def transform_api_task(df_json):
        transform_api(df_json)

    @task
    def merge_task(df_json_db, df_json_api):
        return merge(df_json_db, df_json_api)

    @task
    def load_task(db_data):
        location_json = db_data["location"]
        date_json = db_data["date"]
        attackCharacteristics_json = db_data["attackCharacteristics"]
        perpetratorCharacteristics_json = db_data["perpetratorCharacteristics"]
        disorderType_json = db_data["disorderType"]
        df_json = db_data["df"]
        return load(location_json, date_json, attackCharacteristics_json, perpetratorCharacteristics_json, disorderType_json, df_json)
    

    data_db = extract_raw_db_task()
    data_api = extract_api_task()
    transformed_data_db = transform_db_task(data_db)
    transformed_data_api = transform_api_task(data_api)
    merge_data = merge_task(transformed_data_db, transformed_data_api)
    load_task(transformed_data_db)
    
global_terrorism_dag = gta_dag()