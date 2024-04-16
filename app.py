import pandas as pd
import streamlit as st
from PIL import Image


st.title('Análisis de datos de Sensores en Mi Ciudad')
image = Image.open('grafana2.jpg')
st.image(image)

uploaded_file = st.file_uploader('Choose a file')
if uploaded_file is not None:
   df1=pd.read_csv(uploaded_file)
   st.write(df1)
   st.subheader('Estadísticos básicos de los sensores.')
   st.dataframe(df1["temperatura ESP32"].describe())
   min_temp = st.slider('Selecciona la temperatura mínima (°C)', min_value=-10, max_value=45, value=23)
   # Filtrar el DataFrame utilizando query
   filtrado_df = df1.query(f"`temperatura ESP32` > {min_temp}")
   # Mostrar el DataFrame filtrado
   st.subheader("Temperaturas superiores al valor configurado.")
   st.write('Dataframe Filtrado')
   st.write(filtrado_df)

else:
 st.warning('Necesitas cargar un archivo csv excel.')
