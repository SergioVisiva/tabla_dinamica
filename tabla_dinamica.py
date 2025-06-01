import streamlit as st
import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import plotly.express as px

# ------------------ Generación de datos ------------------
st.set_page_config(layout="wide")

np.random.seed(42)
random.seed(42)

categorias = ['Hamburguesas', 'Bebidas', 'Complementos', 'Postres']
productos = {
    'Hamburguesas': ['Clásica', 'Doble Queso', 'Vegana', 'BBQ'],
    'Bebidas': ['Coca Cola', 'Inka Cola', 'Agua', 'Jugo'],
    'Complementos': ['Papas Fritas', 'Aros de Cebolla', 'Nuggets'],
    'Postres': ['Helado', 'Brownie', 'Pie de Manzana']
}
medios_pago = ['Efectivo', 'Tarjeta', 'Yape', 'Plin']
sucursales = ['San Miguel', 'Miraflores', 'La Molina']

data = []
for _ in range(15):
    categoria = random.choice(categorias)
    producto = random.choice(productos[categoria])
    cantidad = np.random.randint(1, 20)
    precio = round(np.random.uniform(5.0, 25.0), 2)
    total = round(cantidad * precio, 2)
    fecha = datetime.now() - timedelta(days=np.random.randint(0, 30))
    medio_pago = random.choice(medios_pago)
    sucursal = random.choice(sucursales)
    cliente_frecuente = random.choice(['Sí', 'No'])
    data.append({
        "Fecha": fecha.date(),
        "Categoría": categoria,
        "Producto": producto,
        "Cantidad": cantidad,
        "Precio Unitario": precio,
        "Total": total,
        "Medio de Pago": medio_pago,
        "Sucursal": sucursal,
        "Cliente Frecuente": cliente_frecuente
    })

df = pd.DataFrame(data)

# ------------------ Filtros ------------------
st.title("📊 Dashboard de Ventas - Leo's Burguer")
st.markdown("Visualización dinámica con tabla y gráficos")

with st.sidebar:
    st.header("Filtros")
    cat_filter = st.multiselect("Categoría", df["Categoría"].unique(), default=df["Categoría"].unique())
    suc_filter = st.multiselect("Sucursal", df["Sucursal"].unique(), default=df["Sucursal"].unique())
    pago_filter = st.multiselect("Medio de Pago", df["Medio de Pago"].unique(), default=df["Medio de Pago"].unique())

# Aplicar filtros
filtered_df = df[
    (df["Categoría"].isin(cat_filter)) &
    (df["Sucursal"].isin(suc_filter)) &
    (df["Medio de Pago"].isin(pago_filter))
]

# ------------------ KPIs ------------------
col1, col2, col3 = st.columns(3)
col1.metric("💰 Total Ventas", f"S/ {filtered_df['Total'].sum():,.2f}")
col2.metric("📦 Total Productos", f"{filtered_df['Cantidad'].sum()}")
col3.metric("🧾 N° Transacciones", f"{filtered_df.shape[0]}")

# ------------------ Gráfico de barras ------------------
fig = px.bar(
    filtered_df.groupby("Producto")["Total"].sum().reset_index(),
    x="Producto",
    y="Total",
    color="Producto",
    title="Ventas por Producto",
    text_auto=True
)
fig.update_layout(xaxis_title="", yaxis_title="Total (S/)", showlegend=False)
st.plotly_chart(fig, use_container_width=True)

# ------------------ Tabla tabular con colores ------------------
st.markdown("### 🧮 Detalle de Transacciones")
def color_cantidad(val):
    if val < 10:
        return 'background-color: red; color: white'
    elif val < 15:
        return 'background-color: yellow; color: black'
    else:
        return 'background-color: green; color: white'

styled_table = filtered_df.style.applymap(color_cantidad, subset=['Cantidad'])
st.dataframe(styled_table, use_container_width=True)
