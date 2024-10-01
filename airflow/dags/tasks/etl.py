# Importing the necessary modules
# --------------------------------

from database.db_operations import creating_engine, load_clean_data

from extract.extract_db import extracting_db_data
from extract.extract_api import extracting_api_data

from transform.transform_db import transforming_db_data
from transform.transform_api import transforming_api_data
from transform.merge import merging_data

engine = creating_engine()

import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# Creating tasks functions
# ------------------------

def extract_db():
    """
    Extract the raw data from the database.
        
    """
    try:
        df = extracting_db_data()
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")


def extract_api():
    """
    Extraction of the API.
    
    """
    try:
        df = extracting_api_data()
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting API data: {e}")


def transform_db(df_json):
    """
    Function to define the DWH schema.
    
    """
    try:        
        json_data = json.loads(df_json)
        raw_data = pd.DataFrame(json_data)
        location, date, attackCharacteristics, perpetratorCharacteristics, disorderType, factTable = transforming_db_data(raw_data)
        
        return location.to_json(orient="records"), date.to_json(orient="records"), attackCharacteristics.to_json(orient="records"), perpetratorCharacteristics.to_json(orient="records"), disorderType.to_json(orient="records"), factTable.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error defining DWH schema from JSON: {e}")
        return None, None, None, None, None, None


def transform_api(df_json):
    """
    Transform the data extracted from the API.
        
    """
    
    try:
        json_data = json.loads(df_json)
        df = pd.DataFrame(json_data)    
        df = transforming_api_data(df)
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
        df_db = pd.DataFrame(json_data_db)
        
        json_data_api = json.loads(df_json_api)
        df_api = pd.DataFrame(json_data_api)
        
        df = merging_data(df_db, df_api)
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error merging data: {e}")


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
        
        load_clean_data(engine, location, "location")
        load_clean_data(engine, date, "date")
        load_clean_data(engine, attackCharacteristics, "attack_characteristics")
        load_clean_data(engine, perpetratorCharacteristics, "perpetrator_characteristics")
        load_clean_data(engine, disorderType, "disorder_type")
        load_clean_data(engine, df, "fact_table")

        logging.info("Data successfully loaded.")
    except Exception as e:
        logging.error(f"Error loading data: {e}")
        return None