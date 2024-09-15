# Importing the necessary modules
# --------------------------------

from src.database.database import creating_engine, create_table

import json
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


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
        logging.error(f"Error retrieving data: {e}")
        
def uploading_test(df_json):
    
    engine = creating_engine()
    
    json_data = json.loads(df_json)
    
    df = pd.DataFrame(json_data)
    df = df[0:10]
    
    try:
        with engine.connect() as conn:
            create_table(conn, df, "test_pipeline")
        
        return logging.info("Table succesfully created!")
        
    except Exception as e:
        logging.error(f"Error retrieving data: {e}")