import pandas as pd
import streamlit as st
from PIL import Image
import numpy as np
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Análisis de Sensores - Mi Ciudad",
    page_icon="📊",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stAlert {
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Title and description
st.title('📊 Análisis de datos de Sensores en Mi Ciudad')
st.markdown("""
    Esta aplicación permite analizar datos de sensores de temperatura y otros parámetros
    recolectados en diferentes puntos de la ciudad.
""")

# Create map data for EAFIT
eafit_location = pd.DataFrame({
    'lat': [6.2006],
    'lon': [-75.5783],
    'location': ['Universidad EAFIT']
})

# Display map
st.subheader("📍 Ubicación de los Sensores - Universidad EAFIT")
st.map(eafit_location, zoom=15)

# Image display
try:
    image = Image.open('grafana2.jpg')
    st.image(image, caption='Dashboard de Sensores', use_column_width=True)
except FileNotFoundError:
    st.warning('Imagen no encontrada. Verifique la ruta del archivo.')

# File uploader
uploaded_file = st.file_uploader('Seleccione archivo CSV', type=['csv'])

if uploaded_file is not None:
    try:
        # Load and process data
        df1 = pd.read_csv(uploaded_file)
        df1['Time'] = pd.to_datetime(df1['Time'])
        df1 = df1.set_index('Time')

        # Create tabs for different analyses
        tab1, tab2, tab3, tab4 = st.tabs(["📈 Visualización", "📊 Estadísticas", "🔍 Filtros", "🗺️ Información del Sitio"])

        with tab1:
            st.subheader('Visualización de Datos')
            
            # Chart type selector
            chart_type = st.selectbox(
                "Seleccione tipo de gráfico",
                ["Línea", "Área", "Barra"]
            )
            
            # Create plot based on selection
            if chart_type == "Línea":
                st.line_chart(df1["temperatura ESP32"])
            elif chart_type == "Área":
                st.area_chart(df1["temperatura ESP32"])
            else:
                st.bar_chart(df1["temperatura ESP32"])

            # Raw data display with toggle
            if st.checkbox('Mostrar datos crudos'):
                st.write(df1)

        with tab2:
            st.subheader('Análisis Estadístico')
            
            # Statistical summary
            stats_df = df1["temperatura ESP32"].describe()
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.dataframe(stats_df)
            
            with col2:
                # Additional statistics
                st.metric("Temperatura Promedio", f"{stats_df['mean']:.2f}°C")
                st.metric("Temperatura Máxima", f"{stats_df['max']:.2f}°C")
                st.metric("Temperatura Mínima", f"{stats_df['min']:.2f}°C")

        with tab3:
            st.subheader('Filtros de Temperatura')
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Minimum temperature filter
                min_temp = st.slider(
                    'Temperatura mínima',
                    float(df1["temperatura ESP32"].min()),
                    float(df1["temperatura ESP32"].max()),
                    float(df1["temperatura ESP32"].mean()),
                    key="min_temp"
                )
                
                filtrado_df_min = df1.query(f"`temperatura ESP32` > {min_temp}")
                st.write("Registros con temperatura superior a", min_temp, "°C:")
                st.dataframe(filtrado_df_min)
                
            with col2:
                # Maximum temperature filter
                max_temp = st.slider(
                    'Temperatura máxima',
                    float(df1["temperatura ESP32"].min()),
                    float(df1["temperatura ESP32"].max()),
                    float(df1["temperatura ESP32"].mean()),
                    key="max_temp"
                )
                
                filtrado_df_max = df1.query(f"`temperatura ESP32` < {max_temp}")
                st.write("Registros con temperatura inferior a", max_temp, "°C:")
                st.dataframe(filtrado_df_max)

            # Download filtered data
            if st.button('Descargar datos filtrados'):
                csv = filtrado_df_min.to_csv().encode('utf-8')
                st.download_button(
                    label="Descargar CSV",
                    data=csv,
                    file_name='datos_filtrados.csv',
                    mime='text/csv',
                )

        with tab4:
            st.subheader("Información del Sitio de Medición")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("### Ubicación del Sensor")
                st.write("**Universidad EAFIT**")
                st.write("- Latitud: 6.2006")
                st.write("- Longitud: -75.5783")
                st.write("- Altitud: ~1,495 metros sobre el nivel del mar")
            
            with col2:
                st.write("### Detalles del Sensor")
                st.write("- Tipo: ESP32")
                st.write("- Variable medida: Temperatura")
                st.write("- Frecuencia de medición: Según configuración")
                st.write("- Ubicación: Campus universitario")

    except Exception as e:
        st.error(f'Error al procesar el archivo: {str(e)}')
else:
    st.warning('Por favor, cargue un archivo CSV para comenzar el análisis.')
    
# Footer
st.markdown("""
    ---
    Desarrollado para el análisis de datos de sensores urbanos.
    Ubicación: Universidad EAFIT, Medellín, Colombia
""")
