from kafka import KafkaProducer
from sqlalchemy import create_engine
import pandas as pd
import json
import time

engine = create_engine(
    "postgresql+psycopg2://cristiancolorado@localhost:5432/etl_accidentes"
)

producer = KafkaProducer(
    bootstrap_servers="localhost:9092",
    value_serializer=lambda v: json.dumps(v).encode("utf-8")
)

print("🚀 Producer iniciado")

while True:

    total = pd.read_sql(
        """
        SELECT COUNT(*) total
        FROM fact_accidentes
        """,
        engine
    ).iloc[0]["total"]

    lluvia = pd.read_sql(
        """
        SELECT COUNT(*) total
        FROM fact_accidentes f
        JOIN dim_clima c
        ON f.clima_id = c.clima_id
        WHERE c.precipitacion > 0
        """,
        engine
    ).iloc[0]["total"]

    temperatura = pd.read_sql(
        """
        SELECT ROUND(
            AVG(temperatura)::numeric,
            2
        ) temperatura
        FROM dim_clima
        """,
        engine
    ).iloc[0]["temperatura"]

    mensaje = {
        "timestamp": time.strftime(
            "%Y-%m-%d %H:%M:%S"
        ),
        "total_accidentes": int(total),
        "accidentes_lluvia": int(lluvia),
        "temperatura_promedio": float(temperatura)
    }

    producer.send(
        "accidentes_metrics",
        mensaje
    )

    producer.flush()

    print("\n📤 Mensaje enviado")
    print(mensaje)

    time.sleep(10)