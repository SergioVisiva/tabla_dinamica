import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

st.set_page_config(page_title="Dashboard Profesional de Pedidos", layout="wide")
st.title("Dashboard Profesional de Pedidos")

np.random.seed(42)
data = {
    "PedidoID": range(1, 16),
    "Cliente": np.random.choice(["Juan", "Ana", "Luis", "María", "Pedro"], 15),
    "Producto": np.random.choice(["Hamburguesa", "Papas Fritas", "Refresco", "Ensalada"], 15),
    "Cantidad": np.random.randint(1, 10, 15),
    "Precio Unitario": np.round(np.random.uniform(5, 20, 15), 2),
    "Fecha": pd.date_range(start="2025-05-01", periods=15, freq="D"),
    "Estado": np.random.choice(["Entregado", "Pendiente", "Cancelado"], 15),
    "Categoría": np.random.choice(["Comida", "Bebida", "Extra"], 15)
}
df = pd.DataFrame(data)
df["Total"] = df["Cantidad"] * df["Precio Unitario"]

# Filtros en sidebar
st.sidebar.header("Filtros")
cliente_filter = st.sidebar.multiselect("Cliente", df["Cliente"].unique(), df["Cliente"].unique())
producto_filter = st.sidebar.multiselect("Producto", df["Producto"].unique(), df["Producto"].unique())
estado_filter = st.sidebar.multiselect("Estado", df["Estado"].unique(), df["Estado"].unique())
categoria_filter = st.sidebar.multiselect("Categoría", df["Categoría"].unique(), df["Categoría"].unique())

df_filtrado = df[
    (df["Cliente"].isin(cliente_filter)) &
    (df["Producto"].isin(producto_filter)) &
    (df["Estado"].isin(estado_filter)) &
    (df["Categoría"].isin(categoria_filter))
]

def color_cantidad(val):
    if val < 3:
        color = 'red'
    elif val < 7:
        color = 'orange'
    else:
        color = 'green'
    return f'background-color: {color}; color: white; font-weight: bold'

# KPIs
kpi1, kpi2, kpi3, kpi4 = st.columns(4)
kpi1.metric("Pedidos Filtrados", len(df_filtrado))
kpi2.metric("Ingreso Total", f"${df_filtrado['Total'].sum():,.2f}")
kpi3.metric("Cantidad Total", df_filtrado["Cantidad"].sum())
kpi4.metric("Clientes Únicos", df_filtrado["Cliente"].nunique())

st.markdown("---")

# Primera fila: Tabla y gráfico barras lado a lado
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Datos Filtrados")
    st.dataframe(df_filtrado.style.applymap(color_cantidad, subset=['Cantidad']), height=350)

with col2:
    fig_producto = px.bar(
        df_filtrado.groupby("Producto")["Total"].sum().reset_index(),
        x="Producto", y="Total",
        title="Ingresos por Producto",
        text_auto=True,
        color="Producto",
       

