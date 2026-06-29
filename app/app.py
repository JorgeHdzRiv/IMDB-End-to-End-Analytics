import streamlit as st
import pandas as pd
from google.oauth2 import service_account
from google.cloud import bigquery

# 1. Configuración de la página
st.set_page_config(page_title="IMDb Analytics Explorer", page_icon="🎬", layout="wide")

st.title("🎬 Explorador de Películas IMDb (1980-2026)")
st.markdown("Esta aplicación consulta datos en tiempo real desde Google BigQuery mediante SQL, permitiendo explorar los patrones clave de la industria cinematográfica.")

# 2. Conexión a BigQuery (Usando caché para optimizar recursos)
@st.cache_resource
def get_bigquery_client():
    path_credenciales = './imdb-analytics-portfolio-9146f96d121c.json'
    credentials = service_account.Credentials.from_service_account_file(path_credenciales)
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)
    return client

client = get_bigquery_client()

# Reemplaza 'tu-proyecto.imdb_data.movies_clean' con el ID real de tu tabla
tabla_bq = 'imdb-analytics-portfolio.imdb_data.movies_clean'

# 3. Interfaz de Usuario: Barra Lateral de Filtros (Sidebar)
st.sidebar.header("Filtros de Búsqueda")

genero_seleccionado = st.sidebar.selectbox(
    "Selecciona un Género", 
    ["Todos", "Action", "Adventure","Animation","Comedy","Crime","Documentary","Drama","Family",
    "Fantasy","History", "Horror","Musical","Mistery","News","Roamnce","Sci-Fi","Sport","Suspense",
    "Thriller","War","Western"]
)

st.sidebar.markdown("---")
votos_minimos = st.sidebar.slider(
    "Votos Mínimos (Engagement)", 
    min_value=5000, 
    max_value=2000000, 
    value=100000, 
    step=10000
)

st.sidebar.markdown("---")
rango_duracion = st.sidebar.slider(
    "Rango de Duración (minutos)", 
    min_value=60, 
    max_value=240, 
    value=(140, 240)
)

# Función centralizada para ejecutar consultas (Cacheada para no cobrar de más en GCP)
@st.cache_data
def run_query(query):
    return client.query(query).to_dataframe()

# ==========================================
# SECCIÓN 1: Resultados Generales por Género
# ==========================================
if genero_seleccionado == "Todos":
    query_general = f"""
        SELECT title, year, genres, average_rating, runtime_minutes, num_votes
        FROM `{tabla_bq}`
        ORDER BY average_rating DESC, num_votes DESC
        LIMIT 50
    """
else:
    query_general = f"""
        SELECT title, year, genres, average_rating, runtime_minutes, num_votes
        FROM `{tabla_bq}`
        WHERE genres LIKE '%{genero_seleccionado}%'
        ORDER BY average_rating DESC, num_votes DESC
        LIMIT 50
    """

st.subheader(f"🏆 Top 50 películas ({genero_seleccionado})")
with st.spinner("Consultando en BigQuery..."):
    df_resultados = run_query(query_general)
    st.dataframe(df_resultados, width='stretch')

    if not df_resultados.empty:
        st.bar_chart(data=df_resultados, x='title', y='average_rating',horizontal=True,sort=False)

# ==========================================
# SECCIÓN 2: Tendencia Histórica (Impacto 2020)
# ==========================================
st.markdown("---")
st.subheader("📈 Tendencia Histórica de Producción")
query_tendencia = f"""
    SELECT year, COUNT(*) as total_movies, AVG(average_rating) as avg_rating 
    FROM `{tabla_bq}` 
    GROUP BY year 
    ORDER BY year ASC
"""
df_tendencia = run_query(query_tendencia)
st.line_chart(data=df_tendencia, x='year', y='total_movies')

# ==========================================
# SECCIÓN 3: Fenómenos de Masas
# ==========================================
st.markdown("---")
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"🔥 Engagement Extremo (> {votos_minimos:,} votos)")
    query_masas = f"""
        SELECT title, year, average_rating, num_votes 
        FROM `{tabla_bq}`
        WHERE num_votes >= {votos_minimos}
        ORDER BY average_rating DESC
        LIMIT 15
    """
    df_masas = run_query(query_masas)
    st.dataframe(df_masas, width='stretch')

# ==========================================
# SECCIÓN 4: El Mito de la Duración
# ==========================================
with col2:
    st.subheader(f"⏳ Duración: {rango_duracion[0]} - {rango_duracion[1]} min")
    query_duracion = f"""
        SELECT title, runtime_minutes, average_rating 
        FROM `{tabla_bq}`
        WHERE runtime_minutes BETWEEN {rango_duracion[0]} AND {rango_duracion[1]}
        ORDER BY average_rating DESC
        LIMIT 100
    """
    df_duracion = run_query(query_duracion)
    if not df_duracion.empty:
        st.scatter_chart(data=df_duracion, x='runtime_minutes', y='average_rating')
    else:
        st.info("No hay suficientes datos en este rango para graficar.")