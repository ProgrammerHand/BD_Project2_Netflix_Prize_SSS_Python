import argparse
import time
from kafka import KafkaConsumer

def main(topic_name, kafka_bootstrap_server):
    print("Params: ", topic_name, " ", kafka_bootstrap_server)
    # setting up Kafka consumer configuration
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers=kafka_bootstrap_server,
        key_deserializer=lambda m: m.decode('utf-8'),
        value_deserializer=lambda m: m.decode('utf-8')
    )

    print(f"Subscribed to topic: {topic_name} with bootstrap server {kafka_bootstrap_server}")

    try:
        while True:
            # Polling messages
            data = consumer.poll(timeout_ms=6000)
            for topic_partition, records in data.items():
                for record in records:
                    print(record.value)
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing consumer")
    finally:
        consumer.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Kafka Consumer")
    parser.add_argument("topic_name", help="Name of the Kafka topic to subscribe to")
    parser.add_argument("bootstrap_server", help="Bootstrap servers for Kafka")

    args = parser.parse_args()

    main(args.topic_name, args.bootstrap_server)