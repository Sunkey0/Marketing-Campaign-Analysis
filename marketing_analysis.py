import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Datos de ejemplo para campañas de marketing
datos_marketing = {
    'Campaña': ['Campaña A', 'Campaña B', 'Campaña C', 'Campaña D'],
    'Impresiones': [10000, 15000, 12000, 8000],
    'Clics': [500, 750, 600, 400],
    'Conversiones': [50, 75, 60, 40],
    'Costo': [1000, 1500, 1200, 800]
}
df_marketing = pd.DataFrame(datos_marketing)

# Calcular métricas de marketing
df_marketing['CTR (%)'] = (df_marketing['Clics'] / df_marketing['Impresiones']) * 100
df_marketing['Tasa de Conversión (%)'] = (df_marketing['Conversiones'] / df_marketing['Clics']) * 100
df_marketing['CPA ($)'] = df_marketing['Costo'] / df_marketing['Conversiones']

# Datos de ejemplo para ventas
datos_ventas = {
    'Cliente': ['Cliente 1', 'Cliente 2', 'Cliente 3', 'Cliente 1', 'Cliente 2', 'Cliente 3'],
    'Fecha': pd.to_datetime(['2023-01-01', '2023-01-02', '2023-01-03', '2023-02-01', '2023-02-02', '2023-02-03']),
    'Monto': [100, 200, 150, 300, 250, 400]
}
df_ventas = pd.DataFrame(datos_ventas)

# Configuración de Streamlit
st.set_page_config(page_title="Análisis de Campañas de Marketing", layout="wide")
st.title("Análisis de Campañas de Marketing")

# Mostrar métricas de marketing
st.header("Métricas de Marketing")
st.write(df_marketing)

# Gráfico de CTR por campaña
st.header("CTR por Campaña")
fig_ctr = px.bar(df_marketing, x='Campaña', y='CTR (%)', title='CTR por Campaña')
st.plotly_chart(fig_ctr, use_container_width=True)

# Gráfico de Tasa de Conversión por campaña
st.header("Tasa de Conversión por Campaña")
fig_conversion = px.bar(df_marketing, x='Campaña', y='Tasa de Conversión (%)', title='Tasa de Conversión por Campaña')
st.plotly_chart(fig_conversion, use_container_width=True)

# Gráfico de CPA por campaña
st.header("Costo por Adquisición (CPA) por Campaña")
fig_cpa = px.bar(df_marketing, x='Campaña', y='CPA ($)', title='Costo por Adquisición (CPA) por Campaña')
st.plotly_chart(fig_cpa, use_container_width=True)

# Segmentación de Audiencias
st.header("Segmentación de Audiencias")
st.write("### Segmentación por Frecuencia de Compra")
frecuencia_compra = df_ventas.groupby('Cliente')['Fecha'].nunique().reset_index()
frecuencia_compra.columns = ['Cliente', 'Frecuencia de Compra']
st.write(frecuencia_compra)

# Análisis de Cohortes
st.header("Análisis de Cohortes")
df_ventas['Mes'] = df_ventas['Fecha'].dt.to_period('M').astype(str)
cohortes = df_ventas.groupby(['Cliente', 'Mes']).size().unstack()
st.write("### Retención de Clientes por Mes")
st.write(cohortes)

# Modelo de Atribución
st.header("Modelo de Atribución")
st.write("### Asignación de Crédito por Canal de Marketing")
canales_marketing = {
    'Canal': ['Email', 'Redes Sociales', 'Buscadores', 'Display'],
    'Conversiones': [30, 50, 40, 20]
}
df_canales = pd.DataFrame(canales_marketing)

# Modelo de Atribución Lineal
df_canales['Crédito Lineal'] = df_canales['Conversiones'] / df_canales['Conversiones'].sum()
st.write("#### Atribución Lineal")
st.write(df_canales)

# Modelo de Atribución de Primer Contacto
df_canales['Crédito Primer Contacto'] = [1 if i == 0 else 0 for i in range(len(df_canales))]
st.write("#### Atribución de Primer Contacto")
st.write(df_canales)

# Modelo de Atribución de Último Contacto
df_canales['Crédito Último Contacto'] = [1 if i == len(df_canales) - 1 else 0 for i in range(len(df_canales))]
st.write("#### Atribución de Último Contacto")
st.write(df_canales)
