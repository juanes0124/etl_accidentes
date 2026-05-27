import pandas as pd
import numpy as np

# =========================================================
# LIMPIEZA DE ACCIDENTES
# =========================================================

def clean_accidents(df):

    print("\n[CLEAN] Limpiando accidentes...")

    df = df.copy()

    # eliminar duplicados
    df.drop_duplicates(inplace=True)

    # convertir fecha
    df["FECHA_ACCIDENTE"] = pd.to_datetime(
        df["FECHA_ACCIDENTE"],
        errors="coerce"
    )

    # eliminar fechas nulas
    df.dropna(subset=["FECHA_ACCIDENTE"], inplace=True)

    # rango válido
    df = df[
        (df["FECHA_ACCIDENTE"].dt.year >= 2010) &
        (df["FECHA_ACCIDENTE"].dt.year <= 2025)
    ]

    # columnas texto
    columnas_texto = [
        "DEPARTAMENTO_ACCIDENTE",
        "MUNICIPIO_ACCIDENTE",
        "TIPO_VEHICULO",
        "MARCA_VEHICULO",
        "GRAVEDAD_ACCIDENTE",
        "CLASE_ACCIDENTE",
        "ZONA",
        "VIA",
        "CONDICION_VIA"
    ]

    for col in columnas_texto:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.upper()
                .str.strip()
            )

            df[col] = df[col].replace("NAN", np.nan)

    # reemplazar vacíos
    for col in columnas_texto:
        if col in df.columns:
            df[col] = df[col].fillna("DESCONOCIDO")

    # edad vehículo
    if "EDAD_VEHICULO" in df.columns:

        df["EDAD_VEHICULO"] = pd.to_numeric(
            df["EDAD_VEHICULO"],
            errors="coerce"
        )

        mediana = df["EDAD_VEHICULO"].median()

        df["EDAD_VEHICULO"] = (
            df["EDAD_VEHICULO"]
            .fillna(mediana)
            .clip(lower=0)
        )

    print(f"✅ Accidentes limpios: {len(df):,}")

    return df


# =========================================================
# LIMPIEZA DE CLIMA
# =========================================================

def clean_weather(df):

    print("\n[CLEAN] Limpiando clima...")

    df = df.copy()

    # fecha
    df["fecha"] = pd.to_datetime(
        df["fecha"],
        errors="coerce"
    )

    df.dropna(subset=["fecha"], inplace=True)

    # normalizar departamento
    df["departamento"] = (
        df["departamento"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    # columnas numéricas
    columnas_numericas = [
        "hum_relativa",
        "precipitacion",
        "temperatura",
        "vel_viento"
    ]

    for col in columnas_numericas:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

        df[col] = df[col].fillna(df[col].median())

    print(f"✅ Clima limpio: {len(df):,}")

    return df


# =========================================================
# VARIABLES DERIVADAS
# =========================================================

def transform_data(df):

    print("\n[TRANSFORM] Creando variables derivadas...")

    df = df.copy()

    # tiempo
    df["anio"] = df["FECHA_ACCIDENTE"].dt.year
    df["mes"] = df["FECHA_ACCIDENTE"].dt.month
    df["dia"] = df["FECHA_ACCIDENTE"].dt.day
    df["hora"] = df["FECHA_ACCIDENTE"].dt.hour

    # día semana
    df["dia_semana"] = df["FECHA_ACCIDENTE"].dt.day_name()

    # fin de semana
    df["es_fin_semana"] = (
        df["FECHA_ACCIDENTE"].dt.dayofweek >= 5
    )

    # grupo horario
    df["grupo_horario"] = pd.cut(
        df["hora"],
        bins=[0, 6, 12, 18, 24],
        labels=["Madrugada", "Mañana", "Tarde", "Noche"],
        right=False
    )

    # fecha sola
    df["fecha_solo"] = (
        df["FECHA_ACCIDENTE"]
        .dt.strftime("%Y-%m-%d")
    )

    print("✅ Variables creadas")

    return df


# =========================================================
# DIMENSION TIEMPO
# =========================================================

def build_dim_tiempo(df):

    dim = df[[
        "FECHA_ACCIDENTE",
        "anio",
        "mes",
        "dia",
        "hora",
        "grupo_horario",
        "dia_semana",
        "es_fin_semana"
    ]].drop_duplicates().reset_index(drop=True)

    dim.columns = [
        "fecha",
        "anio",
        "mes",
        "dia",
        "hora",
        "grupo_horario",
        "dia_semana",
        "es_fin_semana"
    ]

    dim.insert(0, "tiempo_id", range(1, len(dim) + 1))

    return dim


# =========================================================
# DIMENSION UBICACION
# =========================================================

def build_dim_ubicacion(df):

    dim = df[[
        "DEPARTAMENTO_ACCIDENTE",
        "MUNICIPIO_ACCIDENTE"
    ]].drop_duplicates().reset_index(drop=True)

    dim.columns = [
        "departamento",
        "municipio"
    ]

    dim.insert(0, "ubicacion_id", range(1, len(dim) + 1))

    return dim


# =========================================================
# DIMENSION VEHICULO
# =========================================================

def build_dim_vehiculo(df):

    columnas = [
        "TIPO_VEHICULO",
        "MARCA_VEHICULO",
        "MODELO_VEHICULO",
        "EDAD_VEHICULO"
    ]

    columnas_existentes = [
        c for c in columnas if c in df.columns
    ]

    dim = df[columnas_existentes] \
        .drop_duplicates() \
        .reset_index(drop=True)

    nombres = [
        "tipo_vehiculo",
        "marca",
        "modelo",
        "edad"
    ]

    dim.columns = nombres[:len(columnas_existentes)]

    dim.insert(0, "vehiculo_id", range(1, len(dim) + 1))

    return dim


# =========================================================
# DIMENSION GRAVEDAD
# =========================================================

def build_dim_gravedad(df):

    dim = df[[
        "GRAVEDAD_ACCIDENTE"
    ]].drop_duplicates().reset_index(drop=True)

    dim.columns = ["gravedad"]

    severidad = {
        "MUERTO": "ALTA",
        "HERIDO": "MEDIA",
        "SOLO DAÑOS": "BAJA"
    }

    dim["nivel_severidad"] = dim["gravedad"].map(
        severidad
    ).fillna("DESCONOCIDA")

    dim.insert(0, "gravedad_id", range(1, len(dim) + 1))

    return dim


# =========================================================
# DIMENSION CLIMA
# =========================================================

def build_dim_clima(df):

    dim = df.copy()

    dim = dim.drop_duplicates(
        subset=["departamento", "fecha"]
    ).reset_index(drop=True)

    dim.insert(0, "clima_id", range(1, len(dim) + 1))

    return dim


# =========================================================
# FACT TABLE
# =========================================================

def build_fact(
    df,
    dim_tiempo,
    dim_ubicacion,
    dim_vehiculo,
    dim_gravedad,
    dim_clima
):

    print("\n[FACT] Construyendo fact table...")

    f = df.copy()

    # -------------------------------------
    # JOIN TIEMPO
    # -------------------------------------

    f = f.merge(
        dim_tiempo[[
            "tiempo_id",
            "fecha",
            "hora",
            "grupo_horario"
        ]],
        left_on=[
            "FECHA_ACCIDENTE",
            "hora",
            "grupo_horario"
        ],
        right_on=[
            "fecha",
            "hora",
            "grupo_horario"
        ],
        how="left"
    )

    # -------------------------------------
    # JOIN UBICACION
    # -------------------------------------

    f = f.merge(
        dim_ubicacion,
        left_on=[
            "DEPARTAMENTO_ACCIDENTE",
            "MUNICIPIO_ACCIDENTE"
        ],
        right_on=[
            "departamento",
            "municipio"
        ],
        how="left"
    )

    # -------------------------------------
    # JOIN VEHICULO
    # -------------------------------------

    columnas_left = [
        c for c in [
            "TIPO_VEHICULO",
            "MARCA_VEHICULO",
            "MODELO_VEHICULO",
            "EDAD_VEHICULO"
        ]
        if c in f.columns
    ]

    columnas_right = [
        "tipo_vehiculo",
        "marca",
        "modelo",
        "edad"
    ][:len(columnas_left)]

    f = f.merge(
        dim_vehiculo,
        left_on=columnas_left,
        right_on=columnas_right,
        how="left"
    )

    # -------------------------------------
    # JOIN GRAVEDAD
    # -------------------------------------

    f = f.merge(
        dim_gravedad[[
            "gravedad_id",
            "gravedad"
        ]],
        left_on="GRAVEDAD_ACCIDENTE",
        right_on="gravedad",
        how="left"
    )

    # -------------------------------------
    # PREPARAR CLIMA
    # -------------------------------------

    dim_clima["fecha"] = (
        pd.to_datetime(dim_clima["fecha"])
        .dt.strftime("%Y-%m-%d")
    )

    # -------------------------------------
    # JOIN CLIMA
    # -------------------------------------

    f = f.merge(
        dim_clima[[
            "clima_id",
            "departamento",
            "fecha"
        ]],
        left_on=[
            "DEPARTAMENTO_ACCIDENTE",
            "fecha_solo"
        ],
        right_on=[
            "departamento",
            "fecha"
        ],
        how="left"
    )

    # -------------------------------------
    # FACT TABLE
    # -------------------------------------

    fact = f[[
        "tiempo_id",
        "ubicacion_id",
        "vehiculo_id",
        "gravedad_id",
        "clima_id"
    ]].copy()

    fact["cantidad"] = 1

    print(f"✅ Fact table creada: {len(fact):,}")

    return fact


# =========================================================
# RUN TRANSFORM
# =========================================================

def run_transform(df_accidentes, df_clima):

    # limpieza
    df_accidentes = clean_accidents(df_accidentes)
    df_clima = clean_weather(df_clima)

    # transformación
    df_accidentes = transform_data(df_accidentes)

    # dimensiones
    dim_tiempo = build_dim_tiempo(df_accidentes)

    dim_ubicacion = build_dim_ubicacion(df_accidentes)

    dim_vehiculo = build_dim_vehiculo(df_accidentes)

    dim_gravedad = build_dim_gravedad(df_accidentes)

    dim_clima = build_dim_clima(df_clima)

    # fact
    fact = build_fact(
        df_accidentes,
        dim_tiempo,
        dim_ubicacion,
        dim_vehiculo,
        dim_gravedad,
        dim_clima
    )

    return (
        dim_tiempo,
        dim_ubicacion,
        dim_vehiculo,
        dim_gravedad,
        dim_clima,
        fact
    )