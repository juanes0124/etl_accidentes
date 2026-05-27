# src/queries.py

# ==============================
# KPIs GENERALES
# ==============================

def accidentes_por_anio():

    query = """
    SELECT
        dt.anio,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_tiempo dt
        ON f.tiempo_id = dt.tiempo_id
    GROUP BY dt.anio
    ORDER BY dt.anio;
    """

    return query


def accidentes_por_municipio():

    query = """
    SELECT
        du.municipio,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_ubicacion du
        ON f.ubicacion_id = du.ubicacion_id
    GROUP BY du.municipio
    ORDER BY total_accidentes DESC;
    """

    return query


def accidentes_por_vehiculo():

    query = """
    SELECT
        dv.tipo_vehiculo,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_vehiculo dv
        ON f.vehiculo_id = dv.vehiculo_id
    GROUP BY dv.tipo_vehiculo
    ORDER BY total_accidentes DESC;
    """

    return query


def accidentes_por_gravedad():

    query = """
    SELECT
        dg.gravedad,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_gravedad dg
        ON f.gravedad_id = dg.gravedad_id
    GROUP BY dg.gravedad
    ORDER BY total_accidentes DESC;
    """

    return query


def accidentes_por_rango_anios(inicio, fin):

    query = f"""
    SELECT
        dt.anio,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_tiempo dt
        ON f.tiempo_id = dt.tiempo_id
    WHERE dt.anio BETWEEN {inicio} AND {fin}
    GROUP BY dt.anio
    ORDER BY dt.anio;
    """

    return query


def top_municipios():

    query = """
    SELECT
        du.municipio,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_ubicacion du
        ON f.ubicacion_id = du.ubicacion_id
    GROUP BY du.municipio
    ORDER BY total_accidentes DESC
    LIMIT 10;
    """

    return query


def accidentes_por_departamento():

    query = """
    SELECT
        du.departamento,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_ubicacion du
        ON f.ubicacion_id = du.ubicacion_id
    GROUP BY du.departamento
    ORDER BY total_accidentes DESC;
    """

    return query


def accidentes_por_marca():

    query = """
    SELECT
        dv.marca,
        COUNT(*) AS total_accidentes
    FROM fact_accidentes f
    JOIN dim_vehiculo dv
        ON f.vehiculo_id = dv.vehiculo_id
    GROUP BY dv.marca
    ORDER BY total_accidentes DESC;
    """

    return query


# ==============================
# KPIs CLIMÁTICOS
# ==============================

def accidentes_con_lluvia():

    query = """
    SELECT
        COUNT(*) AS accidentes_con_lluvia
    FROM fact_accidentes f
    JOIN dim_clima dc
        ON f.clima_id = dc.clima_id
    WHERE dc.precipitacion > 0;
    """

    return query


def temperatura_promedio_graves():

    query = """
    SELECT
        dc.departamento,
        ROUND(AVG(dc.temperatura)::numeric,2) AS temperatura_promedio,
        COUNT(*) AS accidentes_graves
    FROM fact_accidentes f
    JOIN dim_clima dc
        ON f.clima_id = dc.clima_id
    JOIN dim_gravedad dg
        ON f.gravedad_id = dg.gravedad_id
    WHERE dg.gravedad IN ('CON HERIDOS','CON MUERTOS')
    GROUP BY dc.departamento
    ORDER BY accidentes_graves DESC;
    """

    return query


def accidentes_lluvia_fuerte():

    query = """
    SELECT
        dc.departamento,
        COUNT(*) AS accidentes_lluvia_fuerte
    FROM fact_accidentes f
    JOIN dim_clima dc
        ON f.clima_id = dc.clima_id
    WHERE dc.precipitacion > 10
    GROUP BY dc.departamento
    ORDER BY accidentes_lluvia_fuerte DESC;
    """

    return query


def humedad_promedio():

    query = """
    SELECT
        ROUND(AVG(dc.hum_relativa)::numeric,2) AS humedad_promedio
    FROM fact_accidentes f
    JOIN dim_clima dc
        ON f.clima_id = dc.clima_id;
    """

    return query


def viento_promedio_muertos():

    query = """
    SELECT
        ROUND(AVG(dc.vel_viento)::numeric,2) AS viento_promedio_muertos
    FROM fact_accidentes f
    JOIN dim_clima dc
        ON f.clima_id = dc.clima_id
    JOIN dim_gravedad dg
        ON f.gravedad_id = dg.gravedad_id
    WHERE dg.gravedad = 'CON MUERTOS';
    """

    return query