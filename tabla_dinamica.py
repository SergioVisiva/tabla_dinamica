import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

st.set_page_config(page_title="Tabla Dinámica", layout="wide")

# Datos de ejemplo
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

# JavaScript para colorear tipo semáforo (verde, amarillo, rojo)
color_cells = JsCode("""
function(params) {
    if (params.value == null) { return {}; }
    if (params.colDef.field == 'Cantidad') {
        if (params.value > 15) { return { 'color': 'white', 'backgroundColor': 'green' }; }
        else if (params.value > 8) { return { 'color': 'black', 'backgroundColor': 'yellow' }; }
        else { return { 'color': 'white', 'backgroundColor': 'red' }; }
    }
    if (params.colDef.field == 'Precio_Unitario') {
        if (params.value > 10) { return { 'color': 'white', 'backgroundColor': 'green' }; }
        else if (params.value > 5) { return { 'color': 'black', 'backgroundColor': 'yellow' }; }
        else { return { 'color': 'white', 'backgroundColor': 'red' }; }
    }
    if (params.colDef.field == 'Total_Venta') {
        if (params.value > 150) { return { 'color': 'white', 'backgroundColor': 'green' }; }
        else if (params.value > 80) { return { 'color': 'black', 'backgroundColor': 'yellow' }; }
        else { return { 'color': 'white', 'backgroundColor': 'red' }; }
    }
    return {};
}
""")

# JavaScript para icono en fecha (emoji calendario)
date_icon = JsCode("""
function(params) {
    if (params.value == null) { return ''; }
    const dateStr = params.value.slice(0,10);  // YYYY-MM-DD
    // Ejemplo: si fecha es fin de semana, rojo; else verde
    const d = new Date(dateStr);
    const day = d.getDay();
    let icon = '📅'; // calendario default
    if (day === 0 || day === 6) {  // domingo o sábado
        icon = '⛔'; // icono de alerta para fines de semana
    }
    return icon + ' ' + dateStr;
}
""")

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)

gb.configure_column("Categoría", rowGroup=True, hide=True)
gb.configure_column("Producto", rowGroup=True, hide=True)

# Aplicar estilos de colores semáforo
gb.configure_column("Cantidad", cellStyle=color_cells)
gb.configure_column("Precio_Unitario", cellStyle=color_cells)
gb.configure_column("Total_Venta", cellStyle=color_cells)

# Aplicar icono a la fecha
gb.configure_column("Fecha", cellRenderer=date_icon)

gb.configure_side_bar()
gb.configure_selection('single')

gridOptions = gb.build()

st.title("Tabla Dinámica con Semáforo y Iconos en Fecha")
st.markdown("Colores en columnas numéricas para identificar rápido y iconos en fecha para observaciones visuales.")

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=500,
    theme="alpine"
)

