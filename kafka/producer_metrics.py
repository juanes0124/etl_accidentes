from kafka import KafkaProducer
from sqlalchemy import create_engine
import pandas as pd
import json
import time

def get_engine():
    user = "etl_user"
    password = "1234"
    host = "localhost"
    port = "5434"
    database = "etl_accidentes"

    engine = create_engine(
        f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}",
        connect_args={
            "options": "-c search_path=etl,public"
        },
        future=True
    )

    return engine


engine = get_engine()

# 🚀 KAFKA PRODUCER
producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Producer iniciado")

while True:

    # 📊 TOTAL ACCIDENTES
    total = pd.read_sql(
        "SELECT COUNT(*) AS total FROM fact_accidentes",
        engine
    ).iloc[0]["total"]

    # 🌧️ ACCIDENTES CON LLUVIA
    lluvia = pd.read_sql(
        """
        SELECT COUNT(*) AS total
        FROM fact_accidentes f
        JOIN dim_clima c ON f.clima_id = c.clima_id
        WHERE c.precipitacion > 0
        """,
        engine
    ).iloc[0]["total"]

    # 🌡️ TEMPERATURA PROMEDIO
    temperatura = pd.read_sql(
        """
        SELECT COALESCE(ROUND(AVG(temperatura)::numeric, 2), 0)
        AS temperatura
        FROM dim_clima
        """,
        engine
    ).iloc[0]["temperatura"]

    # 📦 MENSAJE KAFKA
    mensaje = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total_accidentes": int(total),
        "accidentes_lluvia": int(lluvia),
        "temperatura_promedio": float(temperatura)
    }

    # 📤 ENVIAR A KAFKA
    producer.send("accidentes_metrics", mensaje)
    producer.flush()

    print("\n📤 Mensaje enviado:")
    print(mensaje)

    time.sleep(10)  