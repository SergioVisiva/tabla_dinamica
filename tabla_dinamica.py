import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, JsCode

# Datos simulados
data = {
    "Fecha": ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04"],
    "Categoría": ["Hamburguesas", "Papas", "Bebidas", "Hamburguesas"],
    "Producto": ["Clásica", "Fritas", "Coca-Cola", "Doble carne"],
    "Cantidad": [5, 15, 25, 8],
    "Precio": [15.0, 8.0, 5.0, 20.0]
}
df = pd.DataFrame(data)

# Código JS para pintar la columna "Cantidad"
cellstyle_jscode = JsCode("""
function(params) {
    if (params.value == null) {
        return {};
    }
    if (params.value < 10) {
        return { 'color': 'white', 'backgroundColor': 'red' };
    } else if (params.value < 20) {
        return { 'color': 'black', 'backgroundColor': 'yellow' };
    } else {
        return { 'color': 'white', 'backgroundColor': 'green' };
    }
}
""")

# Configurar tabla con filtros y colores
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(filter=True, sortable=True, resizable=True)
gb.configure_column("Cantidad", cellStyle=cellstyle_jscode)
gridOptions = gb.build()

# Mostrar la tabla
st.title("Tabla con filtros y colores en 'Cantidad'")
AgGrid(df, gridOptions=gridOptions, theme="alpine", fit_columns_on_grid_load=True)

