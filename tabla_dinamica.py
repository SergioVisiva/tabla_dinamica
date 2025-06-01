import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Configuración página
st.set_page_config(page_title="Dashboard Profesional de Pedidos", layout="wide")
st.title("Dashboard Profesional de Pedidos")

# Datos simulados (15 registros)
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

# Panel lateral para filtros
st.sidebar.header("Filtros")
cliente_filter = st.sidebar.multiselect("Cliente", options=df["Cliente"].unique(), default=df["Cliente"].unique())
producto_filter = st.sidebar.multiselect("Producto", options=df["Producto"].unique(), default=df["Producto"].unique())
estado_filter = st.sidebar.multiselect("Estado", options=df["Estado"].unique(), default=df["Estado"].unique())
categoria_filter = st.sidebar.multiselect("Categoría", options=df["Categoría"].unique(), default=df["Categoría"].unique())

# Filtrado
df_filtrado = df[
    (df["Cliente"].isin(cliente_filter)) &
    (df["Producto"].isin(producto_filter)) &
    (df["Estado"].isin(estado_filter)) &
    (df["Categoría"].isin(categoria_filter))
]

# Función para pintar columna 'Cantidad'
def color_cantidad(val):
    if val < 3:
        color = 'red'
    elif val < 7:
        color = 'orange'
    else:
        color = 'green'
    return f'background-color: {color}; color: white; font-weight: bold'

# KPI's en una fila de 4 columnas
st.markdown("### KPIs principales")
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
    # Gráfico barras: Total por Producto
    fig_producto = px.bar(
        df_filtrado.groupby("Producto")["Total"].sum().reset_index(),
        x="Producto",
        y="Total",
        title="Ingresos por Producto",
        text_auto=True,
        color="Producto",
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    fig_producto.update_layout(showlegend=False, margin=dict(t=50, b=30))
    st.plotly_chart(fig_producto, use_container_width=True, height=350)

st.markdown("---")

# Segunda fila: Gráficos pastel y líneas lado a lado
col3, col4 = st.columns(2)

with col3:
    # Gráfico de pastel: Distribución de Estados
    estado_counts = df_filtrado["Estado"].value_counts().reset_index()
    estado_counts.columns = ["Estado", "Cantidad"]

    fig_estado = px.pie(
        estado_counts,
        values="Cantidad",
        names="Estado",
        title="Distribución de Estados de Pedidos",
        color_discrete_sequence=px.colors.sequential.RdBu
    )
    st.plotly_chart(fig_estado, use_container_width=True, height=350)

with col4:
    # Gráfico de líneas: Cantidad de pedidos por fecha
    cantidad_fecha = df_filtrado.groupby("Fecha")["Cantidad"].sum().reset_index()

    fig_lineas = px.line(
        cantidad_fecha,
        x="Fecha",
        y="Cantidad",
        title="Cantidad de Pedidos por Fecha",
        markers=True,
        color_discrete_sequence=["#636EFA"]
    )
    fig_lineas.update_layout(margin=dict(t=50, b=30))
    st.plotly_chart(fig_lineas, use_container_width=True, height=350)

st.markdown("---")

# Tercera fila: Tabla resumen agrupada (ocupa todo ancho)
st.subheader("Resumen por Categoría y Estado")
tabla_resumen = df_filtrado.groupby(["Categoría", "Estado"]).agg({
    "Cantidad": "sum",
    "Total": "sum"
}).reset_index()
st.dataframe(tabla_resumen.style.format({"Total": "${:,.2f}"}), height=300)

st.markdown("---")
st.markdown("Dashboard creado con Streamlit y Plotly | Impresionante y profesional 💼📊")
