from dotenv import load_dotenv
import sys
import os

load_dotenv(f"{sys.path[0]}/../env/.env")

path = os.getenv("PROJECT_PATH")
email = os.getenv("AIRFLOW_EMAIL")

sys.path.append(f"{path}")


# Libraries to work with Airflow
# --------------------------------

from datetime import datetime, timedelta
from airflow.decorators import dag, task

# Importing the necessary modules and env variables
# --------------------------------

from dags.tasks.gta_etl import *


default_args = {
    'owner': "airflow",
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 5),
    'email': f"{email}",
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

@dag(
    default_args=default_args,
    description='Creating an ETL pipeline for out GTA database.',
    schedule='@daily',
)

def gta_dag():
    """
    This DAG is going to execute the ETL pipeline for the Global Terrorism Analysis project.
    
    """
    @task
    def extract_raw_db():
        return extract_raw_db()
    
    extract_raw_db()
    
global_terrorism_dag = gta_dag()