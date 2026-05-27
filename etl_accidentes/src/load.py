import pandas as pd

def load_to_postgres(df, table_name, engine):

    print(f"\n[LOAD] Cargando tabla: {table_name}")

    df.to_sql(
        name=table_name,   # ✅ correcto
        con=engine,
        schema="etl",
        if_exists="replace",
        index=False
    )

    print(f"✅ {table_name} cargada correctamente")