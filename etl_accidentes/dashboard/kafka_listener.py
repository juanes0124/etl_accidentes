from kafka import KafkaConsumer
import json

def get_latest_metric():

    consumer = KafkaConsumer(
        "accidentes_metrics",
        bootstrap_servers="localhost:9092",
        auto_offset_reset="latest",
        consumer_timeout_ms=2000,
        value_deserializer=lambda x: json.loads(x.decode("utf-8"))
    )

    ultimo = None

    for mensaje in consumer:
        ultimo = mensaje.value

    consumer.close()

    return ultimo