from airflow import DAG
from airflow.providers.standard.operators.bash import BashOperator
from datetime import datetime

with DAG(
    dag_id="etl_accidentes_pipeline",
    start_date=datetime(2025, 1, 1),
    catchup=False,
    schedule=None,
    description="Pipeline ETL Accidentes + Clima + Great Expectations"
) as dag:

    run_etl = BashOperator(
        task_id="run_etl_pipeline",
        bash_command="""
        cd /Users/cristiancolorado/etl_accidentes/etl_accidentes &&
        /Users/cristiancolorado/etl_accidentes/venv/bin/python main.py
        """
    )