from src.extract import extract_accidents
from src.extract_clima import extract_climate
from src.transform import run_transform
from src.load import load_to_postgres
from src.db_connection import get_engine

# Validación
from validations.gx_validator import validate_fact_table

# =========================
# RUTAS
# =========================

ACCIDENTES_PATH = "etl_accidentes/data/accidentes.csv"
CLIMA_PATH = "etl_accidentes/data/clima/processed/clima_unificado.csv"

# =========================
# EXTRACT
# =========================

df_accidentes = extract_accidents(ACCIDENTES_PATH)
df_clima = extract_climate(CLIMA_PATH)

# =========================
# TRANSFORM
# =========================

(
    dim_tiempo,
    dim_ubicacion,
    dim_vehiculo,
    dim_gravedad,
    dim_clima,
    fact_accidentes
) = run_transform(
    df_accidentes,
    df_clima
)

# =========================
# VALIDATION
# =========================

print("\n[VALIDATION] Ejecutando validaciones...")

validate_fact_table(fact_accidentes)

# =========================
# CONNECTION
# =========================

engine = get_engine()

# =========================
# LOAD
# =========================

print("\n[LOAD] Cargando tablas a PostgreSQL...")

load_to_postgres(dim_tiempo, "dim_tiempo", engine)
load_to_postgres(dim_ubicacion, "dim_ubicacion", engine)
load_to_postgres(dim_vehiculo, "dim_vehiculo", engine)
load_to_postgres(dim_gravedad, "dim_gravedad", engine)
load_to_postgres(dim_clima, "dim_clima", engine)
load_to_postgres(fact_accidentes, "fact_accidentes", engine)

print("\n🎉 DATA WAREHOUSE CARGADO EN POSTGRESQL")