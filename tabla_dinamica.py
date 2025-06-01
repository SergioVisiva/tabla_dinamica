import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Dashboard Impresionante", layout="wide", page_icon="🚀")

st.title("🚀 Dashboard Profesional y Dinámico")

# Dataset ampliado 15 registros, con categorías, estados, fechas, precios y cantidades
data = {
    "Categoría": ["Hamburguesas", "Hamburguesas", "Hamburguesas", "Papas", "Papas", "Bebidas", "Bebidas", "Postres", "Postres", "Hamburguesas", "Papas", "Bebidas", "Postres", "Hamburguesas", "Bebidas"],
    "Producto": ["Leos Clásica", "Doble Queso", "Vegetariana", "Papas Fritas", "Papas con Queso", "Coca Cola", "Sprite", "Helado Vainilla", "Brownie", "Leos BBQ", "Papas Cajún", "Fanta", "Cheesecake", "Leos Especial", "Agua Mineral"],
    "Cantidad": [25, 40, 18, 50, 35, 60, 55, 20, 15, 30, 40, 25, 10, 22, 50],
    "Precio Unitario": [7.5, 9.0, 8.0, 3.5, 4.0, 2.0, 2.0, 5.0, 4.5, 8.5, 3.8, 2.2, 5.5, 9.5, 1.5],
    "Fecha Pedido": pd.to_datetime([
        "2025-05-01", "2025-05-01", "2025-05-02", "2025-05-02", "2025-05-03",
        "2025-05-03", "2025-05-04", "2025-05-04", "2025-05-05", "2025-05-05",
        "2025-05-06", "2025-05-06", "2025-05-07", "2025-05-07", "2025-05-07"
    ]),
    "Estado": ["Entregado", "Entregado", "Pendiente", "Entregado", "Pendiente",
               "Entregado", "Entregado", "Pendiente", "Cancelado", "Entregado",
               "Entregado", "Pendiente", "Cancelado", "Entregado", "Entregado"]
}

df = pd.DataFrame(data)
df["Total"] = df["Cantidad"] * df["Precio Unitario"]

# --- SIDEBAR FILTROS ---
st.sidebar.header("Filtros de Datos")

categoria_seleccionada = st.sidebar.multiselect(
    "Selecciona Categoría",
    options=df["Categoría"].unique(),
    default=df["Categoría"].unique()
)

estado_seleccionado = st.sidebar.multiselect(
    "Selecciona Estado",
    options=df["Estado"].unique(),
    default=df["Estado"].unique()
)

df_filtrado = df.query(
    "Categoría == @categoria_seleccionada and Estado == @estado_seleccionado"
)

# --- KPI CARDS ---
col1, col2, col3, col4 = st.columns(4)

total_ventas = df_filtrado["Total"].sum()
total_pedidos = df_filtrado.shape[0]
promedio_precio = df_filtrado["Precio Unitario"].mean()
total_cantidad = df_filtrado["Cantidad"].sum()

col1.metric("💰 Total Ventas", f"${total_ventas:,.2f}")
col2.metric("📦 Total Pedidos", total_pedidos)
col3.metric("📊 Precio Promedio", f"${promedio_precio:.2f}")
col4.metric("🍔 Cantidad Total", total_cantidad)

st.markdown("---")

# --- TABLA CON COLORES CONDICIONALES ---
gb = GridOptionsBuilder.from_dataframe(df_filtrado)
gb.configure_default_column(filterable=True, sortable=True, resizable=True)
# Pintar columna cantidad (color semáforo)
cellstyle_jscode = """
function(params) {
    if (params.value == null) {return {};}
    if (params.value < 20) {return {'color': 'white', 'backgroundColor': 'red'};}
    else if (params.value < 40) {return {'color': 'black', 'backgroundColor': 'yellow'};}
    else {return {'color': 'white', 'backgroundColor': 'green'};}
}
"""
gb.configure_column("Cantidad", cellStyle=cellstyle_jscode)
gb.configure_column("Total", type=["numericColumn", "numberColumnFilter", "customNumericFormat"], precision=2)
gridOptions = gb.build()

st.subheader("📋 Tabla Detallada con Filtros")
AgGrid(df_filtrado, gridOptions=gridOptions, enable_enterprise_modules=True, theme="alpine", fit_columns_on_grid_load=True)

# --- GRAFICOS ---
st.markdown("---")
st.subheader("📊 Análisis Visual")

# Ventas totales por categoría (barras)
fig_cat = px.bar(df_filtrado.groupby("Categoría")["Total"].sum().reset_index(),
                 x="Categoría", y="Total",
                 color="Categoría",
                 title="Ventas Totales por Categoría",
                 text_auto=".2s",
                 color_discrete_sequence=px.colors.qualitative.Bold)
st.plotly_chart(fig_cat, use_container_width=True)

# Evolución de ventas por fecha (líneas)
fig_fecha = px.line(df_filtrado.groupby("Fecha Pedido")["Total"].sum().reset_index(),
                   x="Fecha Pedido", y="Total",
                   markers=True,
                   title="Evolución de Ventas por Fecha",
                   color_discrete_sequence=["#636EFA"])
st.plotly_chart(fig_fecha, use_container_width=True)

# Estado de pedidos (pastel)
fig_estado = px.pie(df_filtrado["Estado"].value_counts().reset_index(),
                    values="Estado", names="index",
                    title="Distribución de Estados de Pedidos",
                    color_discrete_sequence=px.colors.sequential.RdBu)
st.plotly_chart(fig_estado, use_container_width=True)

# Ventas vs cantidad scatter
fig_scatter = px.scatter(df_filtrado,
                         x="Cantidad", y="Total",
                         color="Categoría",
                         size="Cantidad",
                         hover_data=["Producto", "Estado"],
                         title="Relación Cantidad vs Ventas")
st.plotly_chart(fig_scatter, use_container_width=True)

# --- CONCLUSIÓN ---
st.markdown("---")
st.info("📌 Usa los filtros en la barra lateral para explorar los datos dinámicamente. Cada visual se actualizará automáticamente.")


