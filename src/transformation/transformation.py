from src.database.database import creating_engine, create_table
import pandas as pd

def general_cleaning(df):
    """
    The general cleaning of the df with EDA help
    
    """
    
    columns_choice = [
    "eventid",
    "iyear",
    "imonth",
    "iday",
    "extended",
    "country_txt",
    "country",
    "region_txt",
    "region",
    "city",
    "latitude",
    "longitude",
    "vicinity",
    "crit1",
    "crit2",
    "crit3",
    "doubtterr",
    "multiple",
    "success",
    "suicide",
    "attacktype1_txt",
    "attacktype1",
    "targtype1_txt",
    "targtype1",
    "natlty1_txt",
    "natlty1",
    "gname",
    "guncertain1",
    "individual",
    "nperpcap",
    "claimed",
    "weaptype1_txt",
    "weaptype1",
    "nkill",
    "property",
    "ishostkid",
    "INT_ANY"
    ]

    defect_values = {
        'nperpcap':0,
        'claimed': 999,
        'nkill':0
    }

    df = df[columns_choice]
    df = df.replace([-9, -99, -999], 999)
    df = df.fillna(value=defect_values)
    df = df.dropna()

    df = df[df['iday'] != 0]
    df = df.query("doubtterr == 0")
    return df

def load_clean():
    """
    Load the cleaned data into the database
    
    """
    
    engine = creating_engine()
    df = pd.read_sql_query('SELECT * FROM global_terrorism_db_raw', engine)
    df = general_cleaning(df)
    create_table(engine, df, 'global_terrorism_db_cleaned')

# Checking the data load
# load_clean()