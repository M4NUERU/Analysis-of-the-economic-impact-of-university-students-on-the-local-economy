import streamlit as st
import pandas as st_pd
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Impacto Económico Universitario", layout="wide", page_icon="📈")

# Load Data
@st.cache_data
def load_data():
    csv_path = 'Impacto economico_clean.csv'
    if not os.path.exists(csv_path):
        st.error(f"Dataset not found at: {csv_path}")
        return pd.DataFrame()
    return pd.read_csv(csv_path)

df = load_data()

if df.empty:
    st.stop()

# Header
st.title("📈 Análisis del Impacto Económico de los Estudiantes Universitarios")
st.markdown("Este dashboard interactivo muestra los patrones de gasto y el impacto económico de los estudiantes universitarios en la economía local.")

# Sidebar Filters
st.sidebar.header("Filtros")

# Filter: Resident Type (Local vs Foráneo)
residencias = df['Reside en tunja'].dropna().unique().tolist()
selected_residencia = st.sidebar.multiselect(
    "Tipo de Residente (Reside en Tunja)",
    options=residencias,
    default=residencias
)

# Filter: Budget Range
presupuestos = df['Presupuesto mensual'].dropna().unique().tolist()
# Sort budgets roughly if possible, or just keep unique
selected_presupuesto = st.sidebar.multiselect(
    "Rango de Presupuesto Mensual",
    options=presupuestos,
    default=presupuestos
)

# Apply filters
filtered_df = df[
    (df['Reside en tunja'].isin(selected_residencia)) &
    (df['Presupuesto mensual'].isin(selected_presupuesto))
]

st.sidebar.markdown("---")
st.sidebar.write(f"**Registros filtrados:** {len(filtered_df)} / {len(df)}")

if filtered_df.empty:
    st.warning("No hay datos que coincidan con los filtros seleccionados.")
    st.stop()

# --- Visualizations ---
col1, col2 = st.columns(2)

with col1:
    st.subheader("Distribución por Presupuesto Mensual")
    fig_budget = px.histogram(
        filtered_df, 
        x='Presupuesto mensual', 
        color='Reside en tunja',
        barmode='group',
        title="Estudiantes por Rango de Presupuesto"
    )
    fig_budget.update_xaxes(categoryorder='total descending')
    st.plotly_chart(fig_budget, use_container_width=True)

with col2:
    st.subheader("Categorías de Gasto Principal")
    # Count occurrences of each category
    gasto_counts = filtered_df['Categoria Gastos'].value_counts().reset_index()
    gasto_counts.columns = ['Categoría', 'Cantidad']
    fig_gasto = px.pie(
        gasto_counts, 
        values='Cantidad', 
        names='Categoría', 
        title="Distribución de Gastos Principales",
        hole=0.4
    )
    st.plotly_chart(fig_gasto, use_container_width=True)

st.divider()

col3, col4 = st.columns(2)

with col3:
    st.subheader("Fuentes de Ingreso")
    ingreso_counts = filtered_df['Fuenetes de ingreso'].value_counts().reset_index()
    ingreso_counts.columns = ['Fuente', 'Cantidad']
    fig_ingreso = px.bar(
        ingreso_counts,
        x='Fuente',
        y='Cantidad',
        title="Principales Fuentes de Ingreso",
        color='Fuente'
    )
    st.plotly_chart(fig_ingreso, use_container_width=True)

with col4:
    st.subheader("Trabajo y Estudio")
    trabajo_counts = filtered_df['Trabajo y estudio'].value_counts().reset_index()
    trabajo_counts.columns = ['Situación', 'Cantidad']
    fig_trabajo = px.pie(
        trabajo_counts,
        values='Cantidad',
        names='Situación',
        title="Proporción de Estudiantes que Trabajan",
        hole=0.4
    )
    st.plotly_chart(fig_trabajo, use_container_width=True)

st.markdown("---")
st.markdown("Dashboard creado a partir del análisis en Jupyter Notebook.")
