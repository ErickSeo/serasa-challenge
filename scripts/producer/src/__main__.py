import csv
import json
from kafka import KafkaProducer
from typing import Dict

class KafkaConfig:
    KAFKA_SERVER = 'kafka-api.kafka.svc.cluster.local:9092'  # Endereço do broker Kafka
    TOPIC = 'landing_zone'

class CSVReader:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read_lines(self):
        with open(self.file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                yield row

class KafkaProducerClient:
    def __init__(self):
        self.producer = KafkaProducer(
            bootstrap_servers=KafkaConfig.KAFKA_SERVER,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )

    def send_message(self, topic: str, message: Dict):
        self.producer.send(topic, value=message)
        self.producer.flush()

    def close(self):
        self.producer.close()

def main():
    csv_file_path = 'src/assets/data.csv'
    print(csv_file_path)
    csv_reader = CSVReader(csv_file_path)
    kafka_producer = KafkaProducerClient()

    for line in csv_reader.read_lines():
        kafka_producer.send_message(KafkaConfig.TOPIC, line)
        print(f'Sent message: {line}')

    kafka_producer.close()

if __name__ == "__main__":
    main()