from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
from dotenv import load_dotenv

import os
import logging
import time
import pandas as pd
import requests

load_dotenv("./env/.env")

api_endpoint = os.getenv("API_ENDPOINT")

def create_kafka_producer():
    return KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )

def create_kafka_consumer():
    return KafkaConsumer(
        "GTA_etl_kafka",
        auto_offset_reset='earliest',
        enable_auto_commit=True,
        consumer_timeout_ms=10000,
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers="localhost:9092"
    )

def send_in_batches(producer, data, batch_size=10):
    """
    Send data to Kafka in batches.
    
    Parameters:
        producer (KafkaProducer): The Kafka producer instance.
        data (pd.DataFrame): The data to be sent.
        batch_size (int): The size of each batch.
    """
    data = pd.read_json(data)
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size].to_dict(orient='records')
        producer.send("GTA_etl_kafka", value=batch)
        producer.flush()
        logging.info(f"Batch sent: {batch}")
        time.sleep(4)

def kafka_producer(df):
    producer = create_kafka_producer()
    try:
        send_in_batches(producer, df)
        logging.info("Messages to fact table sent")

        return "Data sent to Kafka topic"
    except Exception as e:
        logging.error(f"Error creating producer: {e}")
        return None

def kafka_consumer():
    logging.info("Starting to create the Kafka Consumer")
    consumer = create_kafka_consumer()
    for m in consumer:
        message = m.value
        logging.info(m.value)
        df = pd.DataFrame(message)
        data = bytes(df.to_json(orient='records'), 'utf-8')
        requests.post(api_endpoint, data)
        logging.info("Data sent to API")

if __name__ == "__main__":
    kafka_consumer()