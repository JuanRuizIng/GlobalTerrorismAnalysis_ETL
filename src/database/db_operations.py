from dotenv import load_dotenv
from sqlalchemy import create_engine, Integer, Float, String, DateTime, inspect, MetaData, Table, Column, BIGINT
from sqlalchemy_utils import database_exists, create_database

import os
import logging
import warnings

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s", datefmt="%m/%d/%Y %I:%M:%S %p")

load_dotenv("./env/.env")

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")

host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")

database = os.getenv("PG_DATABASE")

# Creating the connection engine from the URL made up of the environment variables
def creating_engine():
    url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    
    if not database_exists(url):
        create_database(url)
        logging.info("Database created")
    
    logging.info("Engine created. You can now connect to the database.")
    
    return engine

def disposing_engine(engine):
    engine.dispose()
    logging.info("Engine disposed.")


# Function for infer sql types
def infer_sqlalchemy_type(dtype, column_name):
    """ Map pandas dtype to SQLAlchemy's types """
    
    if column_name == "eventid":
        return BIGINT
    elif "int" in dtype.name:
        return Integer
    elif "float" in dtype.name:
        return Float
    elif "object" in dtype.name:
        return String(500)
    elif "datetime" in dtype.name:
        return DateTime
    else:
        return String(500)


# Function to create table
def load_clean_data(engine, df, table_name, primary_key="eventid"):
    
    logging.info(f"Creating table {table_name} from Pandas DataFrame")
    
    if not inspect(engine).has_table(table_name):
        metadata = MetaData()
        columns = [Column(name,
                          infer_sqlalchemy_type(dtype, name),
                          primary_key=(name == primary_key)) for name, dtype in df.dtypes.items()]
        
        table = Table(table_name, metadata, *columns)
        table.create(engine)

        df.to_sql(table_name, con=engine, if_exists="append", index=False)
        
        logging.info(f"Table {table_name} succesfully created!")
    else:
        warnings.warn(f"Table {table_name} already exists.")