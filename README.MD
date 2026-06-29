# 🎬 End-to-End Data Analytics & Engineering: IMDb Top Movies (1980-2026)

## 📊 Vista Previa del Dashboard 
![](./assets/dashboard.png)

[Dashboard PowerBI](./dashboard/imdb_analytics.pbix)

## 📊 Vista Previa de la App Interactiva
![](./assets/app.png)

[App Interactiva]("https://imdbtopmovies.streamlit.app/")


## 📖 Descripción del Proyecto
Este proyecto implementa un flujo completo (End-to-End) de análisis e ingeniería de datos sobre un conjunto extraído de IMDb, enfocado en largometrajes estrenados entre 1980 y 2026 con más de 5,000 votos. El ecosistema del proyecto abarca desde la limpieza de datos y construcción de un pipeline ETL hacia la nube, hasta el Análisis Exploratorio de Datos (EDA) y el despliegue de interfaces interactivas para el usuario final. 

El objetivo es auditar, limpiar e identificar patrones en la industria cinematográfica, preparando el terreno para futuros modelos predictivos y demostrando la integración de **Python, SQL y arquitecturas Cloud**.

## 🎯 Objetivos y Hallazgos Clave
* **Auditoría y Limpieza:** Tratamiento de valores atípicos (*outliers*) como documentales históricos de más de 9 horas (*Shoah*) e inconsistencias de la plataforma (*Wendigo*). Imputación de géneros faltantes y eliminación de registros corruptos.
* **Impacto de la Pandemia:** Identificación visual de la caída drástica en el volumen de producción y estrenos en el año 2020.
* **El Mito de la Duración:** Se comprobó estadísticamente que las películas de larga duración (> 140 min) mantienen un estándar de calidad superior (calificaciones > 7.5), minimizando la tasa de fracasos críticos.
* **Polarización por Géneros:** Los Documentales y Biografías lideran las calificaciones promedio, mientras que el género de Terror presenta el desempeño más bajo.
* **Validación por Volumen:** Las películas con un engagement masivo (> 100,000 votos) convergen constantemente en calificaciones sobresalientes.

## 🛠️ Herramientas y Tecnologías
* **Lenguaje Core:** Python 3
* **Manipulación y Limpieza:** Pandas, NumPy
* **Data Warehouse & SQL:** Google BigQuery (Almacenamiento en la nube y consultas)
* **Desarrollo Web Frontend:** Streamlit
* **Inteligencia de Negocio (BI):** Power BI
* **Visualización de Datos:** Matplotlib, Seaborn, Plotly
* **Control de Versiones:** Git & GitHub

## 📂 Estructura del Repositorio
* `/assets/`: Recursos gráficos y capturas de pantalla del proyecto.
* `/data/raw/`: Datos originales (inmutables).
* `/data/processed/`: Datos limpios locales (copia de seguridad).
* `/src/data_cleaning.py`: Script ETL en Python para limpiar datos e inyectarlos directamente a Google BigQuery.
* `/app/app.py`: Aplicación web interactiva desarrollada en Streamlit que consulta la base de datos en la nube vía SQL.
* `/notebooks/01_eda_imdb.ipynb`: Cuaderno de Jupyter con el paso a paso de la exploración estadística.
* `/dashboard/imdb_analytics.pbix`: Tablero interactivo de análisis visual.
* `requirements.txt`: Dependencias necesarias para el entorno de Python.

## 🚀 Cómo ejecutar este proyecto
1. **Clona este repositorio:**  
```bash
git clone "https://github.com/JorgeHdzRiv/IMDB-End-to-End-Analytics.git"
```
2. **Instala las dependencias:** 
```bash
pip install -r requirements.txt`
```
3. **Configura las credenciales (Cloud):**
* Debes tener un proyecto en Google Cloud con BigQuery habilitado.
* Coloca tu archivo de credenciales `JSON` en la raíz del proyecto (¡Asegúrate de que esté listado en tu archivo `.gitignore` para no subirlo a GitHub!).

4. **Ejecuta el pipeline de limpieza:**
```bash
cd src
python data_cleaning.py
```
5. **Lanza la Aplicación Web (Streamlit):**
```bash
cd app
streamlit run app.py
```
6. **Explora los resultados:**
* Abre Jupyter Notebook o JupyterLab y ejecuta el archivo dentro de la carpeta /notebooks.
* Interactúa con la web app en http://localhost:8501.
* Abre el archivo .pbix en la carpeta /dashboard con Power BI Desktop para interactuar con la visualización.
