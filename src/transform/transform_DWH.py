import pandas as pd
import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%d/%m/%Y %I:%M:%S %p")

def transforming_into_DWH(df):
    """
    Function to transform the data from the DB and define the DWH schema
    """
    
    try:
        logging.info("Starting transformation of DB data.")

        # Convert 'date' column to datetime
        logging.info("Converting 'date' column to datetime format.")
        df['date'] = pd.to_datetime(df['date'])

        # Process location data
        logging.info("Extracting location data from DataFrame.")
        location = df[['country', 'country_txt', 'region', 'region_txt', 'city']].copy()
        logging.info("Creating 'id_location' by concatenating country, region, and city.")
        location['id_location'] = (
            location['country'].astype(str) +
            location['region'].astype(str) +
            location['city'].astype(str)
        )
        logging.info("Dropping duplicate entries from location data.")
        location = location.drop_duplicates()
        logging.info("Dropping 'country' and 'region' columns from location data.")
        location = location.drop(['country', 'region'], axis=1)
        logging.info("Renaming columns in location data.")
        location = location.rename(columns={'country_txt': 'country', 'region_txt': 'region'})
        logging.info("Reordering columns in location data.")
        location = location[['id_location', 'country', 'region', 'city']]
        logging.info("Dropping NaN values from location data.")
        location = location.dropna()

        # Process date data
        logging.info("Processing date data.")
        date = df[['date']].copy()
        logging.info("Creating 'id_date' by formatting date.")
        date['id_date'] = date['date'].dt.strftime('%Y%m%d')
        logging.info("Dropping duplicate entries from date data.")
        date = date.drop_duplicates()

        # Process attack characteristics data
        logging.info("Processing attack characteristics data.")
        attackCharacteristics = df[['attacktype1', 'attacktype1_txt', 'targtype1', 'targtype1_txt', 'natlty1', 
                                    'natlty1_txt', 'weaptype1', 'weaptype1_txt', 'crit1', 'crit2', 'crit3', 
                                    'INT_ANY']].copy()
        logging.info("Creating 'id_attack' for attack characteristics.")
        attackCharacteristics['id_attack'] = (
            attackCharacteristics['attacktype1'].astype(str) +
            attackCharacteristics['targtype1'].astype(str) +
            attackCharacteristics['natlty1'].astype(str) +
            attackCharacteristics['weaptype1'].astype(str) +
            attackCharacteristics['crit1'].astype(str) +
            attackCharacteristics['crit2'].astype(str) +
            attackCharacteristics['crit3'].astype(str) +
            attackCharacteristics['INT_ANY'].astype(str)
        )
        logging.info("Dropping duplicate entries from attack characteristics.")
        attackCharacteristics = attackCharacteristics.drop_duplicates()
        logging.info("Dropping unused columns from attack characteristics.")
        attackCharacteristics = attackCharacteristics.drop(['attacktype1', 'targtype1', 'natlty1', 'weaptype1'], axis=1)
        logging.info("Renaming columns in attack characteristics.")
        attackCharacteristics = attackCharacteristics.rename(columns={
            'attacktype1_txt': 'attacktype',
            'targtype1_txt': 'targetype',
            'natlty1_txt': 'natlty',
            'weaptype1_txt': 'weaptype'
        })
        logging.info("Dropping NaN values from attack characteristics.")
        attackCharacteristics = attackCharacteristics.dropna()

        # Process perpetrator characteristics data
        logging.info("Processing perpetrator characteristics data.")
        perpetratorCharacteristics = df[['gname', 'individual', 'nperps', 'nperpcap', 'claimed']].copy()
        logging.info("Creating 'id_perpetrator' for perpetrator characteristics.")
        perpetratorCharacteristics['id_perpetrator'] = (
            df["eventid"].astype(str) +
            perpetratorCharacteristics['gname'].astype(str) +
            perpetratorCharacteristics['individual'].astype(str)
        )
        logging.info("Dropping duplicate entries from perpetrator characteristics.")
        perpetratorCharacteristics = perpetratorCharacteristics.drop_duplicates()
        logging.info("Dropping NaN values from perpetrator characteristics.")
        perpetratorCharacteristics = perpetratorCharacteristics.dropna()

        # Process disorder type data
        logging.info("Processing disorder type data.")
        disorderType = df[['disorder_type']].copy()
        logging.info("Creating 'id_disorder' by mapping disorder types.")
        disorderType['id_disorder'] = disorderType['disorder_type'].replace({
            'Political Violence': 1,
            'Political violence': 1,
            'Political Violence; demonstrations': 2,
            'Political Violence; Demonstrations': 2,
            'demonstrations': 3,
            'Demonstrations': 3,
            'Strategic developments': 4,
            'Unknown': 5
        })
        logging.info("Dropping duplicate entries from disorder type data.")
        disorderType = disorderType.drop_duplicates()
        logging.info("Dropping NaN values from disorder type data.")
        disorderType = disorderType.dropna()

        # Update fact table with new IDs
        logging.info("Updating the fact table with new IDs.")
        df['id_location'] = (
            df['country'].astype(str) +
            df['region'].astype(str) +
            df['city'].astype(str)
        )
        df['id_date'] = df['date'].dt.strftime('%Y%m%d')
        df['id_attack'] = (
            df['attacktype1'].astype(str) +
            df['targtype1'].astype(str) +
            df['natlty1'].astype(str) +
            df['weaptype1'].astype(str) +
            df['crit1'].astype(str) +
            df['crit2'].astype(str) +
            df['crit3'].astype(str) +
            df['INT_ANY'].astype(str)
        )
        df['id_perpetrator'] = (
            df["eventid"].astype(str) +
            df['gname'].astype(str) +
            df['individual'].astype(str)
        )
        df['id_disorder'] = df['disorder_type'].replace({
            'Political Violence': 1,
            'Political violence': 1,
            'Political Violence; demonstrations': 2,
            'Political Violence; Demonstrations': 2,
            'demonstrations': 3,
            'Demonstrations': 3,
            'Strategic developments': 4,
            'Unknown': 5
        })
        logging.info("Selecting relevant columns for the fact table.")
        df = df[['eventid', 'extended', 'multiple', 'success', 'suicide', 'nkill', 'property', 'ishostkid', 
                 'nwound', 'id_location', 'id_date', 'id_attack', 'id_perpetrator', 'id_disorder']]
        
        df = df.drop_duplicates(subset=['eventid'])

        logging.info("Transformation complete. Returning DataFrames.")
        return location, date, attackCharacteristics, perpetratorCharacteristics, disorderType, df

    except Exception as e:
        logging.error(f"Error defining DWH schema: {e}")
        return None, None, None, None, None, None