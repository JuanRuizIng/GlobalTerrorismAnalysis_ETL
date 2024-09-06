from dotenv import load_dotenv
import sys
import os

load_dotenv(f"{sys.path[0]}/../../env/.env")

path = os.getenv("PROJECT_PATH")
email = os.getenv("AIRFLOW_EMAIL")

sys.path.append(f"{path}")

# Importing the necessary modules
# --------------------------------

from src.database.database import creating_engine, create_table
from src.rawLoad.raw import *
from src.transformation.transformation import *

import json


# Creating tasks functions
# ------------------------

def extract_raw_db() -> json:
    """
    Extract the raw data from the database
    
    """
    
    engine = creating_engine()

    try:
        # Asegurarse de que el engine es compatible con SQLAlchemy
        df = pd.read_sql_table("global_terrorism_db_cleaned", con=engine)
        print("Data successfully retrieved.")
        return df.to_json(orient="records")
    except Exception as e:
        print(f"Error retrieving data: {e}")

# df = extract_raw_db()
# print(df)