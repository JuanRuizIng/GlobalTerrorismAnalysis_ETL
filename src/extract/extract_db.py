from database.db_operations import creating_engine, disposing_engine

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

## ----- DB Extract ----- ##

def extracting_db_data():
    """
    Extracting data from the GTA table and return it as a DataFrame.   

    """
    engine = creating_engine()
    
    try:
        logging.info("Starting to extract the data from the Global Terrorism table.")
        df = pd.read_sql_table("global_terrorism_db_cleaned", engine)
        logging.info("Data extracted from the Global Terrorism table.")
        
        return df
    except Exception as e:
        logging.error(f"Error extracting data from the Global Terrorism table: {e}.")
    finally:
        disposing_engine(engine)