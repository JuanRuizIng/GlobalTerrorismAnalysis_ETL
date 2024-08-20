import os

from dotenv import load_dotenv
from sqlalchemy import create_engine


# Reading the environment variables
load_dotenv("../env/.env")

driver = os.getenv("PG_DRIVER")

user = os.getenv("PG_USER")
password = os.getenv("PG_PASSWORD")

host = os.getenv("PG_HOST")
port = os.getenv("PG_PORT")

database = os.getenv("PG_DATABASE")

# Creating the connection engine from the URL made up of the environment variables
def creating_engine():
    url = f"{driver}://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(url)
    
    return engine