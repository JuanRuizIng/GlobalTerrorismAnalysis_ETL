from kafka import KafkaProducer, KafkaConsumer
from json import dumps, loads
import logging
import time
import pandas as pd

def create_kafka_producer():
    return KafkaProducer(
        value_serializer=lambda m: dumps(m).encode('utf-8'),
        bootstrap_servers=['localhost:9092'],
    )

def create_kafka_consumer():
    return KafkaConsumer(
        'GTA_etl_kafka',
        enable_auto_commit=True,
        group_id='my-group-1',
        value_deserializer=lambda m: loads(m.decode('utf-8')),
        bootstrap_servers=['localhost:9092']
    )

def send_in_batches(producer, data, batch_size=5):
    """
    Send data to Kafka in batches.
    
    Parameters:
        producer (KafkaProducer): The Kafka producer instance.
        data (pd.DataFrame): The data to be sent.
        batch_size (int): The size of each batch.
    """
    data = pd.read_json(data)
    data = data[["nkill", "nwound"]]
    for i in range(0, len(data), batch_size):
        batch = data.iloc[i:i + batch_size].to_dict(orient='records')
        producer.send("GTA_etl_kafka", value=batch)
        producer.flush()
        logging.info(f"Batch sent: {batch}")
        time.sleep(4)  # Optional: Sleep to simulate delay

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
    consumer = create_kafka_consumer()
    try:
        for m in consumer:
            logging.info(m.value)
    except Exception as e:
        logging.error(f"Error consuming messages: {e}")

#if __name__ == "__main__":
#    kafka_consumer()
    # kafka_producer # Se tendría que hacer así, pero para entregable de proyecto no se hará.