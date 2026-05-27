# Traffic Accidents & Climate Data Engineering Project

## Overview

This project implements a complete **Data Engineering solution** for the analysis of traffic accidents in Colombia by integrating accident records with climate information.

The solution follows a modern data architecture that includes:

- ETL Pipeline developed in Python
- Data Warehouse in PostgreSQL
- Dimensional Modeling (Star Schema)
- Data Quality Validation with Great Expectations
- Workflow Orchestration using Apache Airflow
- Real-Time Streaming with Apache Kafka
- Interactive Analytics Dashboard with Streamlit

The objective is to transform raw accident and weather datasets into a reliable analytical platform for decision-making and traffic safety analysis.

---

# Project Objectives

The project aims to:

- Extract accident and climate data from raw sources
- Clean and standardize inconsistent records
- Integrate weather conditions with accident events
- Build a dimensional Data Warehouse
- Validate data quality automatically
- Generate analytical KPIs
- Automate ETL execution through Airflow
- Stream metrics through Kafka
- Visualize insights through interactive dashboards

---

# Solution Architecture

```text
Traffic Accidents CSV
            │
            ▼
Climate Data CSV
            │
            ▼
     Python ETL Pipeline
            │
 ┌──────────┼──────────┐
 ▼          ▼          ▼
Extract  Transform  Validate
                    (GX)
            │
            ▼
 PostgreSQL Data Warehouse
            │
     ┌──────┴──────┐
     ▼             ▼
 Apache Kafka   SQL KPIs
     │             │
     └──────┬──────┘
            ▼
    Streamlit Dashboard
```

---

# Dimensional Model (Star Schema)

The Data Warehouse follows a dimensional approach based on a Star Schema.

## Fact Table

### fact_accidentes

Contains accident-related metrics and references to dimensions.

| Field |
|---------|
| tiempo_id |
| ubicacion_id |
| vehiculo_id |
| gravedad_id |
| clima_id |
| cantidad |

---

## Dimension Tables

### dim_tiempo

Time dimension used for temporal analysis.

| Field |
|---------|
| tiempo_id |
| fecha |
| anio |
| mes |
| dia |

---

### dim_ubicacion

Geographical information.

| Field |
|---------|
| ubicacion_id |
| departamento |

---

### dim_vehiculo

Vehicle characteristics.

| Field |
|---------|
| vehiculo_id |
| clase_vehiculo |

---

### dim_gravedad

Accident severity categories.

| Field |
|---------|
| gravedad_id |
| gravedad |

---

### dim_clima

Weather conditions associated with accidents.

| Field |
|---------|
| clima_id |
| temperatura |
| humedad |
| viento |
| precipitacion |

---

# Star Schema Diagram

```text
                    dim_tiempo
                    ──────────
                    tiempo_id
                        │
                        │
                        ▼

dim_ubicacion ───► fact_accidentes ◄─── dim_vehiculo
ubicacion_id         cantidad            vehiculo_id
                        ▲
                        │
                        │

               dim_gravedad
               gravedad_id

                        │
                        ▼

                  dim_clima
                  clima_id
```

---

# Data Quality Validation

The project uses **Great Expectations** to validate data quality before loading information into the Data Warehouse.

Implemented validations include:

- Null value detection
- Empty fact table validation
- Foreign key integrity checks
- Invalid climate references detection
- Negative metrics validation

Pipeline execution is automatically stopped when critical validation errors are detected.

---

# ETL Pipeline

## Extract

Data sources:

- Traffic accidents dataset
- Climate dataset

Data is extracted using Pandas and processed into DataFrames.

---

## Transform

Main transformations include:

- Data cleaning
- Missing value handling
- Date normalization
- Climate integration
- Derived variable creation
- Dimensional modeling
- Fact table generation

Additional climate variables such as temperature, humidity, precipitation and wind speed are integrated with accident records.

---

## Validate

Data quality validations are executed using Great Expectations before loading.

Validation rules include:

- Mandatory IDs not null
- Fact table not empty
- Climate IDs valid
- No negative quantities
- Referential consistency checks

---

## Load

The transformed data is loaded into PostgreSQL.

Generated tables:

- dim_tiempo
- dim_ubicacion
- dim_vehiculo
- dim_gravedad
- dim_clima
- fact_accidentes

The final Data Warehouse contains more than 250,000 processed accident records.

---

# Apache Airflow Orchestration

The ETL process is orchestrated using Apache Airflow.

### DAG Structure

```text
etl_accidentes_pipeline
        │
        ▼
run_etl_pipeline
        │
        ▼
main.py
        │
        ▼
Extract → Transform → Validate → Load
```

Airflow provides:

- Workflow scheduling
- Execution monitoring
- Logging
- Error management
- Pipeline automation

The DAG executes the complete ETL process and loads the Data Warehouse automatically.

---

# Apache Kafka Streaming

Apache Kafka was integrated to simulate real-time analytical data streaming.

## Components

- Kafka Broker
- Producer
- Consumer
- Topic

### Topic

```text
accidentes_metrics
```

Kafka enables the publication and consumption of analytical metrics that can be integrated into monitoring dashboards.

---

# Analytical KPIs

The project implements several KPIs for traffic accident analysis.

## General Indicators

- Total accidents
- Accidents by department
- Accidents by vehicle type
- Accidents by severity
- Monthly accident trends
- Temporal evolution of accidents

## Climate Indicators

- Accidents during rainfall
- Average temperature in severe accidents
- Accidents during heavy precipitation
- Average humidity levels
- Wind speed impact on fatal accidents

These KPIs help identify risk factors associated with road safety and environmental conditions.

---

# Interactive Dashboard

An interactive dashboard was developed using Streamlit.

Dashboard features include:

- KPI cards
- Interactive charts
- Climate analytics
- Geographic analysis
- Department filters
- Time-series visualizations
- Interactive maps
- Real-time metric integration

Run dashboard:

```bash
streamlit run dashboard/app.py
```

---

# Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| Data Processing | Pandas |
| Database | PostgreSQL |
| ORM | SQLAlchemy |
| Data Quality | Great Expectations |
| Workflow Orchestration | Apache Airflow |
| Streaming Platform | Apache Kafka |
| Dashboard | Streamlit |
| Visualization | Plotly |
| Analysis | Jupyter Notebook |

---

# Project Structure

```text
etl_accidentes/
│
├── data/
│   ├── accidentes.csv
│   └── clima/
│
├── dashboard/
│
├── notebooks/
│
├── src/
│   ├── extract.py
│   ├── extract_clima.py
│   ├── transform.py
│   ├── load.py
│   ├── db_connection.py
│   ├── menu_kpis.py
│   ├── queries.py
│   └── unir_clima.py
│
├── validations/
│   ├── __init__.py
│   └── gx_validator.py
│
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Installation

Clone repository:

```bash
git clone https://github.com/CristianColorado33/etl_accidentes.git
```

Enter project directory:

```bash
cd etl_accidentes
```

Create virtual environment:

```bash
python3 -m venv venv
```

Activate environment:

### macOS / Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# Running the ETL Pipeline

Execute the complete ETL process:

```bash
python3 main.py
```

The pipeline performs:

1. Data extraction
2. Data transformation
3. Data validation
4. Data Warehouse loading

---

# Running KPI Queries

Execute KPI menu:

```bash
python3 -m src.menu_kpis
```

Available KPIs include:

- Accidents by vehicle type
- Accidents by department
- Severity analysis
- Rainfall-related accidents
- Climate indicators

---

# Running the Dashboard

Launch Streamlit dashboard:

```bash
streamlit run dashboard/app.py
```

Then open:

```text
http://localhost:8501
```

---

# Example SQL Query

Example KPI query:

```sql
SELECT
    departamento,
    SUM(cantidad) AS total_accidentes
FROM fact_accidentes f
JOIN dim_ubicacion u
ON f.ubicacion_id = u.ubicacion_id
GROUP BY departamento
ORDER BY total_accidentes DESC;
```

---

# Academic Concepts Applied

This project applies concepts from:

- Data Engineering
- ETL Pipelines
- Data Warehousing
- Dimensional Modeling
- Data Quality Management
- Workflow Orchestration
- Event Streaming
- Business Intelligence
- Analytical Processing

---

# Author

Cristian Alexis Colorado Muñoz**

Universidad Autónoma de Occidente

Data Engineering Academic Project

---

# License

This project was developed exclusively for academic and educational purposes.