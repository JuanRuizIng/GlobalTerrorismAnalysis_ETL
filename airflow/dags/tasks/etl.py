# Importing the necessary modules
# --------------------------------

from database.db_operations import creating_engine, create_table
from etl.etlFunctions import transform_db, transform_api, merge_function, DWH_definition_function

engine = creating_engine()
from dotenv import load_dotenv
load_dotenv("/home/juanruizing/GlobalTerrorismAnalysis_ETL/src/env/.env")
import json
import os
import pandas as pd
import logging
import requests

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# Creating tasks functions
# ------------------------

def extract_raw_db():
    """
    Extract the raw data from the database.
    
    Returns:
        str: A JSON string containing the extracted data in records orientation.
        
    """
    
    logging.info("Starting to extract the data.")

    try:
        query = 'SELECT * FROM global_terrorism_db_raw'
        df = pd.read_sql_query(query, engine)
        
        logging.info("Data successfully extracted.")
               
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")


def extract_api():
    """
    Extraction of the API 
    """
    api_key = os.getenv("API_KEY")
    api_email = os.getenv("API_EMAIL")
    try:
        url = 'https://api.acleddata.com/acled/read.json'
        params = {
            'key': f'{api_key}',
            'email': f'{api_email}',
            'fields': 'event_date|country|disorder_type|actor1',
            'year': '1989|2017',
            'year_where': 'BETWEEN',
            'limit': 5000,
            'page': 1
        }

        all_records = []

        while True:
            response = requests.get(url, params=params)
            data = response.json()
        
            if 'data' not in data or not data['data']:
                break
        
            all_records.extend(data['data'])
            params['page'] += 1

        df = pd.DataFrame(all_records)
        logging.info("API data successfully extracted.")
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting API data: {e}")


def transform_db(df_json):
    """
    Transform the data extracted from the database.

    Parameters:
        df_json (str): JSON string containing the data to transform.
    
    Returns:
        str: A JSON string containing the transformed data in records orientation.
        
    """
    
    logging.info("Starting to transform the data.")
    
    try:
        if not df_json:
            raise ValueError("Empty JSON string")
        
        json_data = json.loads(df_json)
        df = pd.json_normalize(data=json_data)
        df = transform_db(df)
        logging.info("Data successfully transformed.")
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error transforming data: {e}")


def transform_api(df_json):
    """
    Transform the data extracted from the API.

    Parameters:
        df_json (str): JSON string containing the data to transform.
    
    Returns:
        str: A JSON string containing the transformed data in records orientation.
        
    """
    
    logging.info("Starting to transform the data.")
    
    try:
        if not df_json:
            raise ValueError("Empty JSON string")
        
        json_data = json.loads(df_json)
        df = pd.json_normalize(data=json_data)
        df = transform_api(df)
        logging.info("Data successfully transformed.")
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error transforming data: {e}")


def merge(df_json_db, df_json_api):
    """
    Merge the transformed data from the database and the API.

    Parameters:
        df_json_db (str): JSON string containing the data from the database.
        df_json_api (str): JSON string containing the data from the API.
    
    Returns:
        str: A JSON string containing the merged data in records orientation.
    """
    
    logging.info("Starting to merge the data.")
    
    try:
        if not df_json_db or not df_json_api:
            raise ValueError("Empty JSON string")
        
        json_data_db = json.loads(df_json_db)
        df_db = pd.json_normalize(data=json_data_db)
        
        json_data_api = json.loads(df_json_api)
        df_api = pd.json_normalize(data=json_data_api)
        
        df = merge_function(df_db, df_api)

        logging.info("Data successfully merged.")
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error merging data: {e}")


def DWH_definition(df_json):
    """
    Function to define the DWH schema
    """
    try:
        if not df_json:
            raise ValueError("Empty JSON string")
        
        json_data = json.loads(df_json)
        df = pd.json_normalize(data=json_data)
        location, date, attackCharacteristics, perpetratorCharacteristics, disorderType, df = DWH_definition_function(df)
        return location.to_json(orient="records"), date.to_json(orient="records"), attackCharacteristics.to_json(orient="records"), perpetratorCharacteristics.to_json(orient="records"), disorderType.to_json(orient="records"), df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error defining DWH schema from JSON: {e}")
        return None, None, None, None, None, None


def load(location_json, date_json, attackCharacteristics_json, perpetratorCharacteristics_json, disorderType_json, df_json):
    """
    Load the data into the DWH.
    """
    
    logging.info("Starting to load the data.")
    
    try:
        if not location_json or not date_json or not attackCharacteristics_json or not perpetratorCharacteristics_json or not disorderType_json or not df_json:
            raise ValueError("Empty JSON string")
        
        location = pd.json_normalize(data=json.loads(location_json))
        date = pd.json_normalize(data=json.loads(date_json))
        attackCharacteristics = pd.json_normalize(data=json.loads(attackCharacteristics_json))
        perpetratorCharacteristics = pd.json_normalize(data=json.loads(perpetratorCharacteristics_json))
        disorderType = pd.json_normalize(data=json.loads(disorderType_json))
        df = pd.json_normalize(data=json.loads(df_json))
        
        engine = creating_engine()
        
        create_table(engine, location, "location")
        create_table(engine, date, "date")
        create_table(engine, attackCharacteristics, "attack_characteristics")
        create_table(engine, perpetratorCharacteristics, "perpetrator_characteristics")
        create_table(engine, disorderType, "disorder_type")
        create_table(engine, df, "fact_table")

        logging.info("Data successfully loaded.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None