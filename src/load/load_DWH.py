import pandas as pd
import logging
from database.db_operations import creating_engine, disposing_engine, load_clean_data

def loading_data(location, date, attackCharacteristics, perpetratorCharacteristics, disorderType, df):
    """
    Carga los datos en el DWH.
    """
    
    logging.info("Starting to load the data.")
    
    try:        
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
    finally:
        disposing_engine(engine)