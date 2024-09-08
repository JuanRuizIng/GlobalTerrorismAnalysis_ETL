# Getting the environment variables
# ----------------------------------

from dotenv import load_dotenv

import sys
import os
import logging

load_dotenv(f"{sys.path[0]}/../../env/.env")

path = os.getenv("PROJECT_PATH")
email = os.getenv("AIRFLOW_EMAIL")

sys.path.append(f"{path}")


# Importing the necessary modules
# --------------------------------

from src.database.database import creating_engine, create_table

import json
import pandas as pd
import logging
import warnings

warnings.simplefilter('ignore', UserWarning)


# Creating tasks functions
# ------------------------

def extract_raw_db():
    """
    Extract the raw data from the database
    
    """
    
    engine = creating_engine()

    try:
        with engine.connect() as conn:
            query = 'SELECT * FROM global_terrorism_db_cleaned'
            
            df = pd.read_sql_query(query, conn)
            logging.info("Data successfully retrieved.")
        
        
        return df.to_json(orient="records")
    except Exception as e:
        print(f"Error retrieving data: {e}")


# Example: Loading the data
def uploading_data(df):
    engine = creating_engine()
    
    try:
        with engine.connect() as conn:
            json_data = json.loads(extract_raw_db())
            df = pd.json_normalize(json_data)
            df_cropped = df[0:10]

            create_table(conn, df_cropped, "test")
    except Exception as e:
        print(f"Error retrieving data: {e}")
    
uploading_data(extract_raw_db())