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
    'retry_delay': timedelta(minutes=1)
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
    
    extracted_data = extract_raw_db_task()
    
    @task
    def uploading_data_task(data):
        return uploading_test(data)
    
    uploading_data_task(extracted_data)
    
global_terrorism_dag = gta_dag()