import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

def merging_data(df_db, df_api):
    """
    Merge the transformed data from the database and the API.

    Parameters:
        df_db (DataFrame): DataFrame containing the transformed data from the database.
        df_api (DataFrame): DataFrame containing the transformed data from the API.
    
    Returns:
        DataFrame: Merged DataFrame.
    """
    logging.info(f"df_db columns: {df_db.columns.tolist()}")
    logging.info(f"df_api columns: {df_api.columns.tolist()}")
    
    logging.info("Starting to merge the data.")

    try:
        df = pd.merge(df_db, df_api, how='left', on='date_country_actor')

        df = df.drop(['event_date', 'country_y', 'actor1'], axis=1)
        df = df.rename(columns={'country_x': 'country'})
        df['disorder_type'] = df['disorder_type'].fillna("Unknown")

        logging.info("Data successfully merged.")
        return df
    except Exception as e:
        logging.error(f"Error merging data: {e}")
        return None