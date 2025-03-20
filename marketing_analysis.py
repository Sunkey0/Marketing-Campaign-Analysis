import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st

# Configuración de Streamlit
st.set_page_config(page_title="Análisis de Campañas de Marketing", layout="wide")
st.title("Análisis de Campañas de Marketing")

# Generar datos de ventas masivos
np.random.seed(42)  # Para reproducibilidad
clientes = [f'Cliente {i}' for i in range(1, 101)]  # 100 clientes únicos
fechas = pd.date_range(start='2023-01-01', end='2023-12-31', freq='D')  # Rango de fechas en 2023
montos = np.random.randint(50, 500, size=1000)  # Montos aleatorios entre 50 y 500

# Crear DataFrame de ventas
df_ventas = pd.DataFrame({
    'Cliente': np.random.choice(clientes, size=1000),  # Asignar clientes aleatorios
    'Fecha': np.random.choice(fechas, size=1000),  # Asignar fechas aleatorias
    'Monto': montos  # Montos aleatorios
})

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

# Crear pestañas en Streamlit
tab1, tab2 = st.tabs(["Análisis de Campañas", "Explicación de Métricas"])

with tab1:
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

    # Gráfica de Frecuencia de Compra por Cliente
    fig_frecuencia = px.bar(frecuencia_compra.sort_values(by='Frecuencia de Compra', ascending=False),
                           x='Cliente', y='Frecuencia de Compra', title='Frecuencia de Compra por Cliente')
    st.plotly_chart(fig_frecuencia, use_container_width=True)

    # Análisis de Cohortes
    st.header("Análisis de Cohortes")
    df_ventas['Mes'] = df_ventas['Fecha'].dt.to_period('M').astype(str)
    cohortes = df_ventas.groupby(['Cliente', 'Mes']).size().unstack()
    st.write("### Retención de Clientes por Mes")
    st.write(cohortes)

    # Gráfica de Ventas Acumuladas por Mes
    st.header("Ventas Acumuladas por Mes")
    ventas_mensuales = df_ventas.groupby('Mes')['Monto'].sum().reset_index()
    fig_ventas_mensuales = px.line(ventas_mensuales, x='Mes', y='Monto', title='Ventas Acumuladas por Mes')
    st.plotly_chart(fig_ventas_mensuales, use_container_width=True)

    # Gráfica de Valor de Vida del Cliente (CLV)
    st.header("Valor de Vida del Cliente (CLV)")
    clv = df_ventas.groupby('Cliente')['Monto'].sum().reset_index()
    clv.columns = ['Cliente', 'CLV']
    fig_clv = px.bar(clv.sort_values(by='CLV', ascending=False),
                    x='Cliente', y='CLV', title='Valor de Vida del Cliente (CLV)')
    st.plotly_chart(fig_clv, use_container_width=True)

with tab2:
    st.header("Explicación de Métricas y Modelos")

    st.write("""
    ### Métricas Clave

    1. **CTR (Click-Through Rate)**
    - **Fórmula:** 
      \[
      CTR = \left( \frac{\text{Clics}}{\text{Impresiones}} \right) \times 100
      \]
    - **Interpretación:** Mide el porcentaje de personas que hicieron clic en un anuncio después de verlo.

    2. **Tasa de Conversión**
    - **Fórmula:**
      \[
      \text{Tasa de Conversión} = \left( \frac{\text{Conversiones}}{\text{Clics}} \right) \times 100
      \]
    - **Interpretación:** Mide el porcentaje de clics que resultaron en una conversión.

    3. **CPA (Costo por Adquisición)**
    - **Fórmula:**
      \[
      CPA = \frac{\text{Costo}}{\text{Conversiones}}
      \]
    - **Interpretación:** Indica cuánto cuesta adquirir un cliente.

    4. **CLV (Customer Lifetime Value)**
    - **Fórmula:**
      \[
      CLV = \sum \text{Monto Gastado por Cliente}
      \]
    - **Interpretación:** Representa el valor total que un cliente genera durante su relación con la empresa.

    5. **Retención de Clientes**
    - **Fórmula:**
      \[
      \text{Retención} = \frac{\text{Clientes Activos en el Mes Actual}}{\text{Clientes Activos en el Mes Anterior}}
      \]
    - **Interpretación:** Mide la capacidad de la empresa para retener clientes.

    ### Modelos de Atribución

    1. **Atribución Lineal**
    - **Fórmula:**
      \[
      \text{Crédito por Canal} = \frac{\text{Conversiones del Canal}}{\text{Total de Conversiones}}
      \]
    - **Interpretación:** Asigna crédito equitativo a todos los canales involucrados en una conversión.

    2. **Atribución de Primer Contacto**
    - **Fórmula:**
      \[
      \text{Crédito} = \begin{cases}
      1 & \text{si es el primer canal} \\
      0 & \text{en otro caso}
      \end{cases}
      \]
    - **Interpretación:** Asigna todo el crédito al primer canal que interactuó con el cliente.

    3. **Atribución de Último Contacto**
    - **Fórmula:**
      \[
      \text{Crédito} = \begin{cases}
      1 & \text{si es el último canal} \\
      0 & \text{en otro caso}
      \end{cases}
      \]
    - **Interpretación:** Asigna todo el crédito al último canal antes de la conversión.
    """)
