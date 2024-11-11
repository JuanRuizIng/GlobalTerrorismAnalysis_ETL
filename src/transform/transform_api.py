import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

def transforming_api_data(df):
    """
    Transform the data extracted from the API.

    Parameters:
        df (DataFrame): DataFrame containing the data to transform.
    
    Returns:
        DataFrame: Transformed DataFrame.
    """
    
    logging.info("Starting to transform the data from the API.")
    
    try:
        df = df.dropna()
        df['date_country_actor'] = df['event_date'].astype(str) + df['country'] + df['actor1']
        
        logging.info("Data successfully transformed.")
        
        return df
    except Exception as e:
        logging.error(f"Error transforming data: {e}")
        return None