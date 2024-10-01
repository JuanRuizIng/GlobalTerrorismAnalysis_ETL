import pandas as pd
import logging

def transforming_db_data(df):
    """
    Function to transform the data from the DB and define the DWH schema
    """
    
    try:
        location = df[['country', 'country_txt', 'region', 'region_txt', 'city']]
        location['id_location'] = df['country'].astype(str) + df['region'].astype(str) + df['city'].astype(str)
        location = location.drop_duplicates()
        location = location.drop(['country', 'region'], axis=1)
        location = location.rename(columns={'country_txt': 'country', 'region_txt': 'region'})
        location = location[['id_location', 'country', 'region', 'city']]
        location = location.dropna()

        date = df[['date']].copy()
        date['id_date'] = df['date'].dt.strftime('%Y%m%d')
        date = date.drop_duplicates()

        attackCharacteristics = df[['attacktype1', 'attacktype1_txt', 'targtype1', 'targtype1_txt', 'natlty1', 'natlty1_txt', 'weaptype1', 'weaptype1_txt', 'crit1', 'crit2', 'crit3', 'INT_ANY']].copy()
        attackCharacteristics['id_attack'] = df['attacktype1'].astype(str) + df['targtype1'].astype(str) + df['natlty1'].astype(str) + df['weaptype1'].astype(str) + df['crit1'].astype(str) + df['crit2'].astype(str) + df['crit3'].astype(str) + df['INT_ANY'].astype(str)
        attackCharacteristics = attackCharacteristics.drop_duplicates()
        attackCharacteristics = attackCharacteristics.drop(['attacktype1', 'targtype1', 'natlty1', 'weaptype1'], axis=1)
        attackCharacteristics = attackCharacteristics.rename(columns={'attacktype1_txt': 'attacktype', 'targtype1_txt': 'targetype', 'natlty1_txt': 'natlty', 'weaptype1_txt': 'weaptype'})
        attackCharacteristics = attackCharacteristics.dropna()

        perpetratorCharacteristics = df[['gname', 'individual', 'nperps', 'nperpcap', 'claimed']].copy()
        perpetratorCharacteristics['id_perpetrator'] = df['eventid'].astype(str) + df['gname'].astype(str) 
        perpetratorCharacteristics = perpetratorCharacteristics.drop_duplicates()
        perpetratorCharacteristics = perpetratorCharacteristics.dropna()

        disorderType = df[['disorder_type']].copy()
        disorderType['id_disorder'] = df['disorder_type'].replace({'Political Violence': 1, 'Political Violence; demonstrations': 2, 'demonstrations': 3, 'Strategic developments': 4, 'Unknown': 5})
        disorderType = disorderType.drop_duplicates()
        disorderType = disorderType.dropna()

        df['id_location'] = df['country'].astype(str) + df['region'].astype(str) + df['city'].astype(str)
        df['id_date'] = df['date'].dt.strftime('%Y%m%d')
        df['id_attack'] = df['attacktype1'].astype(str) + df['targtype1'].astype(str) + df['natlty1'].astype(str) + df['weaptype1'].astype(str) + df['crit1'].astype(str) + df['crit2'].astype(str) + df['crit3'].astype(str) + df['INT_ANY'].astype(str)
        df['id_perpetrator'] = df['eventid'].astype(str) + df['gname'].astype(str)
        df['id_disorder'] = df['disorder_type'].replace({'Political Violence': 1, 'Political Violence; demonstrations': 2, 'demonstrations': 3, 'Strategic developments': 4, 'Unknown': 5})
        df = df[['eventid', 'extended', 'multiple', 'success', 'suicide', 'nkill', 'property', 'ishostkid', 'nwound', 'id_location', 'id_date', 'id_attack', 'id_perpetrator', 'id_disorder']]

        return location, date, attackCharacteristics, perpetratorCharacteristics, disorderType, df

    except Exception as e:
        logging.error(f"Error defining DWH schema: {e}")
        return None, None, None, None, None, None