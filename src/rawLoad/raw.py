from src.database.database import creating_engine
import pandas as pd

def load_raw():
    """ 
    Load the raw data into the database
    
    """
    
    df = pd.read_csv('./data/globalterrorismdb_0718dist.csv', low_memory=False, encoding='ISO-8859-1')
    
    engine = creating_engine()
    
    df.to_sql('global_terrorism_db_raw', engine, if_exists='replace', index=False)

# Checking the function
# load_raw()