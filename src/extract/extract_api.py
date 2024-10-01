from dotenv import load_dotenv
import os

import requests
import pandas as pd
import logging

load_dotenv("./env/.env")

api_key = os.getenv("API_KEY")
api_email = os.getenv("API_EMAIL")

import logging
import requests
import pandas as pd

def extracting_api_data():
    try:
        logging.info("Starting API data extraction.")
        
        url = 'https://api.acleddata.com/acled/read.json'
        params = {
            'key': f'{api_key}',
            'email': f'{api_email}',
            'fields': 'event_date|country|disorder_type|actor1',
            'year': '1989|2017',
            'year_where': 'BETWEEN',
            'limit': 5000,
            'page': 1
        }

        all_records = []
        logging.info(f"Requesting data from {url} with initial params {params}")
        
        while True:
            response = requests.get(url, params=params)
            logging.debug(f"Requesting page {params['page']}")
            data = response.json()
        
            if 'data' not in data or not data['data']:
                logging.info(f"No more data found after page {params['page']}.")
                break
            
            logging.info(f"Retrieved {len(data['data'])} records from page {params['page']}.")
            all_records.extend(data['data'])
            params['page'] += 1
            
        df = pd.DataFrame(all_records)
        logging.info(f"API data extraction complete with {len(df)} total records.")
        
        return df
    except Exception as e:
        logging.error(f"Error extracting data: {e}")
