from sqlalchemy import create_engine

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