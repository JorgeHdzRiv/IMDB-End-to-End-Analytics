import pandas as pd
import os
import pandas_gbq
from google.oauth2 import service_account

def load_data(file_path):
    """Carga los datos crudos."""
    print(f"Cargando datos desde: {file_path}")
    return pd.read_csv(file_path)

def clean_runtime(df):
    """
    Elimina registros con nulos en duración (ej. Wendigo) 
    y filtra valores atípicos extremos (ej. Shoah).
    """
    # Eliminar nulo en runtime_minutes (Wendigo)
    df = df.dropna(subset=['runtime_minutes'])
    
    # Eliminar outliers (películas de más de 4 horas como Shoah) para no afectar modelos
    df = df[df['runtime_minutes'] <= 240]
    
    return df

def clean_genres(df):
    """Rellena los valores nulos en la columna genres con el mapeo investigado."""
    generos_reales = {
        'tt7668842': 'Comedy',
        'tt28754073': 'Drama, Musical',
        'tt32135732': 'Action, Drama, Thriller',
        'tt33291804': 'Drama, Suspense',
        'tt29856129': 'Horror, Thriller',
        'tt36329718': 'Drama, Family'
    }
    df['genres'] = df['genres'].fillna(df['imdb_id'].map(generos_reales))
    return df

def upload_to_bigquery(df):
    """Sube el DataFrame limpio a Google BigQuery Sandbox."""
    
    # 1. Ruta al archivo JSON que descargaste (Asegúrate de que esté en .gitignore)
    path_credenciales = './imdb-analytics-portfolio-9146f96d121c.json.'
    credentials = service_account.Credentials.from_service_account_file(path_credenciales)
    
    # 2. Configuración de tu proyecto en GCP
    # Reemplaza 'tu-id-de-proyecto' con el ID real que aparece en GCP
    project_id = 'imdb-analytics-portfolio' 
    table_id = 'imdb_data.movies_clean' # formato: dataset.tabla
    
    print(f"Subiendo {len(df)} registros a BigQuery ({table_id})...")
    
    # 3. Ejecutar la carga
    pandas_gbq.to_gbq(
        df, 
        table_id, 
        project_id=project_id, 
        if_exists='replace', # 'replace' sobrescribe la tabla, ideal para desarrollo
        credentials=credentials
    )
    print("¡Carga exitosa! Los datos ya están disponibles en la nube para consultarlos con SQL.")

def run_cleaning_pipeline(input_path='./data/raw/imdb_top_movies_1980_2026.csv'):
    df = load_data(input_path)
    df = clean_runtime(df)
    df = clean_genres(df)
    df = df.drop_duplicates()
    
    # En lugar de exportar a CSV, ahora mandamos a la nube
    upload_to_bigquery(df)
    
    return df

if __name__ == "__main__":
    run_cleaning_pipeline()