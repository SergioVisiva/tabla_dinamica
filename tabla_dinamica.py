import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from datetime import datetime

# Configuración general
st.set_page_config(page_title="Dashboard de Ventas", layout="wide")
st.markdown(
    """
    <style>
        .main {background-color: #f8f9fa;}
        .block-container {padding-top: 2rem;}
        h1, h2, h3 {color: #1f77b4;}
        .stMetric {background-color: #ffffff !important; border-radius: 12px; padding: 10px;}
    </style>
    """,
    unsafe_allow_html=True
)

# Título
st.title("📊 Dashboard de Ventas - Leos Burguer")
st.markdown("Visualiza tus ventas agrupadas por categoría y producto, como una tabla dinámica jerárquica de Excel.")

# ======================
# 🧾 Datos simulados
# ======================
data = {
    "Categoría": ["Comida", "Comida", "Comida", "Bebida", "Comida", "Bebida"],
    "Producto": ["Hamburguesa", "Hamburguesa", "Papas", "Refresco", "Papas", "Refresco"],
    "Cantidad": [10, 5, 20, 15, 10, 5],
    "Precio_Unitario": [12, 12, 5, 3, 5, 3],
    "Vendedor": ["Luis", "Ana", "Luis", "Ana", "Luis", "Luis"],
    "Fecha": ["2024-05-01", "2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"]
}

df = pd.DataFrame(data)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

# ======================
# 📈 Métricas
# ======================
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🔢 Total de Ventas", f"S/. {df['Total_Venta'].sum():,.2f}")
with col2:
    st.metric("🛍️ Productos Vendidos", df["Cantidad"].sum())
with col3:
    st.metric("👤 Vendedores Activos", df["Vendedor"].nunique())

st.markdown("---")

# ======================
# 📊 Tabla dinámica
# ======================
st.subheader("📁 Tabla Dinámica por Categoría > Producto")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)

# Agrupar por jerarquía: Categoría > Producto
gb.configure_column("Categoría", rowGroup=True, hide=True)
gb.configure_column("Producto", rowGroup=True, hide=True)

# Estética y funcionalidad
gb.configure_side_bar()
gb.configure_selection('single')
gb.configure_grid_options(domLayout='normal', suppressAggFuncInHeader=True)

gridOptions = gb.build()

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=500,
    theme="material"  # Otras opciones: "streamlit", "balham", "alpine"
)
