# Establishing the working directory
# -----------------------------------

import os

try:
    os.chdir('../../GlobalTerrorismAnalysis_ETL')
except FileNotFoundError:
    print("""
        Posiblemente ya ejecutaste este bloque dos o más veces o tal vez el directorio está incorrecto. 
        ¿Ya ejecutaste este bloque antes y funcionó? Recuerda no ejecutarlo de nuevo. 
        ¿Estás en el directorio incorrecto? Puedes cambiarlo. 
        Recuerda el directorio donde estás:
        """)
print(os.getcwd())

# Libraries to work with Airflow
# --------------------------------

from datetime import datetime, timedelta
from airflow import DAG
from airflow.decorators import dag, task

# Importing the necessary modules and env variables
# --------------------------------

from dags.tasks.gta_etl import *

email = os.getenv('AIRFLOW_EMAIL')

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 9, 5),
    'email': [email],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=3)
}

@dag(
    default_args=default_args,
    description='Creating an ETL pipeline for out GTA database.',
    schedule_interval='@daily',
)

def gta_dag():
    """
    This DAG is going to execute the ETL pipeline for the Global Terrorism Analysis project.
    
    """