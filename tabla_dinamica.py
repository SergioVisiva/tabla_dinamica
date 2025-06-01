import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder
from st_aggrid.shared import JsCode

# Datos con la nueva columna 'categoria'
data = [
    {"categoria": "Hamburguesas", "producto": "Classic Burger", "cantidad": 10, "precio": 5.99, "fecha": "2024-05-01"},
    {"categoria": "Hamburguesas", "producto": "Cheese Burger", "cantidad": 5, "precio": 6.49, "fecha": "2024-05-02"},
    {"categoria": "Papas", "producto": "Papas Fritas", "cantidad": 20, "precio": 2.99, "fecha": "2024-05-03"},
    {"categoria": "Papas", "producto": "Papas Gajo", "cantidad": 7, "precio": 3.49, "fecha": "2024-05-04"},
]

df = pd.DataFrame(data)

# Convertimos fecha a string para evitar errores de serialización
df["fecha"] = df["fecha"].astype(str)

# Javascript para colorear celdas según valor (semáforo)
color_cantidad = JsCode("""
function(params) {
    if (params.value >= 15) {
        return { 'color': 'white', 'backgroundColor': 'green' };
    } else if (params.value >= 5) {
        return { 'color': 'black', 'backgroundColor': 'yellow' };
    } else {
        return { 'color': 'white', 'backgroundColor': 'red' };
    }
}
""")

color_precio = JsCode("""
function(params) {
    if (params.value >= 6) {
        return { 'color': 'white', 'backgroundColor': 'green' };
    } else if (params.value >= 3) {
        return { 'color': 'black', 'backgroundColor': 'yellow' };
    } else {
        return { 'color': 'white', 'backgroundColor': 'red' };
    }
}
""")

# Icono simple para la fecha (usamos un emoji)
fecha_icon = JsCode("""
function(params) {
    const date = params.value;
    // Mostrar un icono según día par o impar (solo ejemplo)
    if (date.endsWith('1') || date.endsWith('3') || date.endsWith('5') || date.endsWith('7') || date.endsWith('9')) {
        return '📅 ' + date;
    } else {
        return '🗓️ ' + date;
    }
}
""")

# Configuramos grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("categoria", rowGroup=True, hide=True)
gb.configure_column("producto", rowGroup=True, hide=True)
gb.configure_column("cantidad", cellStyle=color_cantidad)
gb.configure_column("precio", cellStyle=color_precio)
gb.configure_column("fecha", cellRenderer=fecha_icon)

gridOptions = gb.build()

st.title("Tabla dinámica con colores y jerarquía")

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    allow_unsafe_jscode=True,
    theme="alpine"
)


