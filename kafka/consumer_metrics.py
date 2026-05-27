from kafka import KafkaConsumer
import json

consumer = KafkaConsumer(

    "accidentes_metrics",

    bootstrap_servers="localhost:9092",

    auto_offset_reset="latest",

    value_deserializer=lambda x:
        json.loads(
            x.decode("utf-8")
        )
)

print("📡 Escuchando métricas...\n")

for mensaje in consumer:

    data = mensaje.value

    print("\n" + "="*50)

    print(
        f"⏰ {data['timestamp']}"
    )

    print(
        f"🚗 Total accidentes: "
        f"{data['total_accidentes']}"
    )

    print(
        f"🌧️ Accidentes con lluvia: "
        f"{data['accidentes_lluvia']}"
    )

    print(
        f"🌡️ Temperatura promedio: "
        f"{data['temperatura_promedio']} °C"
    )

    print("="*50)