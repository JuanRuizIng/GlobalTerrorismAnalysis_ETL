# Importing the necessary modules
# --------------------------------

from database.db_operations import creating_engine, create_table

import json
import pandas as pd
import logging

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
    
    engine = creating_engine()

    try:
        query = 'SELECT * FROM global_terrorism_db_cleaned'
        df = pd.read_sql_query(query, engine)
        
        logging.info("Data successfully extracted.")
               
        return df.to_json(orient="records")
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
        
def uploading_test(df_json):
    """
    Loads data from a JSON to a database.

    Parameters:
        df_json (str): JSON string containing the data to load.
    
    """
    
    logging.info("Starting to upload the data.")
    
    engine = creating_engine()
    json_data = json.loads(df_json)
    
    df = pd.DataFrame(json_data)
    df = df[0:10]
    
    try:
        create_table(engine, df, "test_pipeline")
        
    except Exception as e:
        logging.error(f"Error uploading data: {e}")