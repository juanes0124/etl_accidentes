import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine
from kafka_listener import get_latest_metric
from streamlit_autorefresh import st_autorefresh


# ==================================================
# CONFIGURACIÓN
# ==================================================

st.set_page_config(
    page_title="DW Accidentes Colombia",
    page_icon="🚗",
    layout="wide"
)

# ==================================================
# ESTILOS
# ==================================================

st.markdown("""
<style>

.main {
    background-color: #f8fafc;
}

h1, h2, h3 {
    color: #0f172a;
}

div[data-testid="metric-container"] {
    background-color: white;
    border: 1px solid #e2e8f0;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

</style>
""", unsafe_allow_html=True)

# ==================================================
# CONEXIÓN
# ==================================================

@st.cache_resource
def get_engine():

    return create_engine(
        "postgresql+psycopg2://cristiancolorado@localhost:5432/etl_accidentes"
    )

engine = get_engine()

# ==================================================
# TÍTULO
# ==================================================

st_autorefresh(
    interval=10000,
    key="kafka_refresh"
)

st.title("🚗 Dashboard de Accidentes de Tránsito")

st.caption(
    "Data Warehouse • PostgreSQL • ETL • Great Expectations • Airflow • Streamlit"
)

# ==================================================
# FILTROS
# ==================================================

st.sidebar.header("🎛️ Filtros")

departamentos = pd.read_sql("""

SELECT DISTINCT departamento
FROM dim_ubicacion
ORDER BY departamento

""", engine)

departamento = st.sidebar.selectbox(
    "Departamento",
    ["Todos"] + departamentos["departamento"].tolist()
)

# ==================================================
# WHERE DINÁMICO
# ==================================================

where = ""

if departamento != "Todos":

    where = f"""
    WHERE u.departamento = '{departamento}'
    """

# ==================================================
# KPIs
# ==================================================

kpis = pd.read_sql(f"""

SELECT

COUNT(*) total_accidentes,

COUNT(DISTINCT u.departamento) departamentos,

COUNT(DISTINCT u.municipio) municipios,

ROUND(
AVG(dc.temperatura)::numeric,
2
) temperatura_promedio

FROM fact_accidentes f

LEFT JOIN dim_ubicacion u
ON f.ubicacion_id = u.ubicacion_id

LEFT JOIN dim_clima dc
ON f.clima_id = dc.clima_id

{where}

""", engine)

total_accidentes = int(kpis["total_accidentes"][0])
total_departamentos = int(kpis["departamentos"][0])
total_municipios = int(kpis["municipios"][0])
temp_promedio = kpis["temperatura_promedio"][0]

st.divider()

st.header("📡 Monitoreo Kafka en Tiempo Real")

data = get_latest_metric()

if data:

    k1,k2,k3 = st.columns(3)

    with k1:
        st.metric(
            "🚗 Total Accidentes",
            data["total_accidentes"]
        )

    with k2:
        st.metric(
            "🌧️ Accidentes con lluvia",
            data["accidentes_lluvia"]
        )

    with k3:
        st.metric(
            "🌡️ Temperatura promedio",
            f"{data['temperatura_promedio']} °C"
        )

    st.caption(
        f"Última actualización: {data['timestamp']}"
    )

else:

    st.warning(
        "No se encontraron métricas Kafka."
    )

# ==================================================
# TARJETAS KPI
# ==================================================

c1,c2,c3,c4 = st.columns(4)

with c1:
    st.metric(
        "🚗 Total Accidentes",
        f"{total_accidentes:,}"
    )

with c2:
    st.metric(
        "🏢 Departamentos",
        total_departamentos
    )

with c3:
    st.metric(
        "📍 Municipios",
        total_municipios
    )

with c4:
    st.metric(
        "🌡️ Temperatura Promedio",
        f"{temp_promedio} °C"
    )

st.divider()

# ==================================================
# ACCIDENTES POR AÑO
# ==================================================

st.subheader("📈 Evolución de Accidentes por Año")

df_anio = pd.read_sql(f"""

SELECT

t.anio,
COUNT(*) accidentes

FROM fact_accidentes f

JOIN dim_tiempo t
ON f.tiempo_id = t.tiempo_id

JOIN dim_ubicacion u
ON f.ubicacion_id = u.ubicacion_id

{where}

GROUP BY t.anio
ORDER BY t.anio

""", engine)

fig1 = px.bar(
    df_anio,
    x="anio",
    y="accidentes",
    text_auto=True,
    title="Accidentes por Año"
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

# ==================================================
# DEPARTAMENTOS Y GRAVEDAD
# ==================================================

col1,col2 = st.columns(2)

# -------------------------

with col1:

    df_dep = pd.read_sql(f"""

    SELECT

    departamento,
    COUNT(*) accidentes

    FROM fact_accidentes f

    JOIN dim_ubicacion u
    ON f.ubicacion_id = u.ubicacion_id

    {where}

    GROUP BY departamento
    ORDER BY accidentes DESC

    """, engine)

    fig2 = px.bar(
        df_dep,
        x="departamento",
        y="accidentes",
        title="🏆 Ranking de Departamentos"
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

# -------------------------

with col2:

    df_gravedad = pd.read_sql(f"""

    SELECT

    gravedad,
    COUNT(*) accidentes

    FROM fact_accidentes f

    JOIN dim_gravedad g
    ON f.gravedad_id = g.gravedad_id

    JOIN dim_ubicacion u
    ON f.ubicacion_id = u.ubicacion_id

    {where}

    GROUP BY gravedad

    """, engine)

    fig3 = px.pie(
        df_gravedad,
        names="gravedad",
        values="accidentes",
        title="⚠️ Distribución por Gravedad"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

# ==================================================
# VARIABLES CLIMÁTICAS
# ==================================================

st.header("🌦️ Variables Climáticas")

cl1,cl2 = st.columns(2)

# -------------------------

with cl1:

    clima = pd.read_sql("""

    SELECT

    departamento,

    ROUND(
        AVG(temperatura)::numeric,
        2
    ) temperatura

    FROM dim_clima

    GROUP BY departamento

    """, engine)

    fig4 = px.bar(
        clima,
        x="departamento",
        y="temperatura",
        title="🌡️ Temperatura Promedio"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

# -------------------------

with cl2:

    lluvia = pd.read_sql("""

    SELECT

    departamento,
    COUNT(*) accidentes

    FROM fact_accidentes f

    JOIN dim_clima c
    ON f.clima_id = c.clima_id

    WHERE c.precipitacion > 20

    GROUP BY departamento

    ORDER BY accidentes DESC

    """, engine)

    fig5 = px.bar(
        lluvia,
        x="departamento",
        y="accidentes",
        title="🌧️ Accidentes con Lluvia Fuerte"
    )

    st.plotly_chart(
        fig5,
        use_container_width=True
    )

# ==================================================
# MAPA INTERACTIVO
# ==================================================

st.header("🗺️ Distribución Geográfica")

coords = pd.DataFrame({

    "departamento": [
        "ANTIOQUIA",
        "ATLANTICO",
        "CUNDINAMARCA",
        "VALLE DEL CAUCA"
    ],

    "lat": [
        6.2442,
        10.9639,
        4.7110,
        3.4516
    ],

    "lon": [
        -75.5812,
        -74.7964,
        -74.0721,
        -76.5320
    ]
})

mapa = pd.read_sql("""

SELECT

u.departamento,
COUNT(*) accidentes

FROM fact_accidentes f

JOIN dim_ubicacion u
ON f.ubicacion_id = u.ubicacion_id

GROUP BY u.departamento

""", engine)

mapa = mapa.merge(
    coords,
    on="departamento",
    how="left"
)

fig_mapa = px.scatter_mapbox(

    mapa,

    lat="lat",
    lon="lon",

    size="accidentes",
    color="accidentes",

    hover_name="departamento",

    hover_data=[
        "accidentes"
    ],

    zoom=4,
    height=600
)

fig_mapa.update_layout(
    mapbox_style="open-street-map"
)

st.plotly_chart(
    fig_mapa,
    use_container_width=True
)

# ==================================================
# TABLA RESUMEN
# ==================================================

st.header("📋 Tabla Resumen")

tabla = pd.read_sql(f"""

SELECT

u.departamento,
g.gravedad,
COUNT(*) accidentes

FROM fact_accidentes f

JOIN dim_ubicacion u
ON f.ubicacion_id = u.ubicacion_id

JOIN dim_gravedad g
ON f.gravedad_id = g.gravedad_id

{where}

GROUP BY
u.departamento,
g.gravedad

ORDER BY accidentes DESC

LIMIT 100

""", engine)

st.dataframe(
    tabla,
    use_container_width=True
)

# ==================================================
# CONCLUSIONES
# ==================================================

st.header("📌 Conclusiones del Análisis")

st.success(
"""
• El Data Warehouse integra exitosamente información de accidentes y clima.

• Antioquia concentra la mayor cantidad de accidentes asociados a registros climáticos.

• Las condiciones de lluvia fuerte muestran una relación significativa con la accidentalidad.

• La temperatura promedio presenta diferencias importantes entre departamentos.

• La solución permite realizar análisis multidimensionales mediante PostgreSQL y Streamlit.
"""
)