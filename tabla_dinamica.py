from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

# Datos
data = {
    "Categoria": ["Hamburguesas", "Hamburguesas", "Papas", "Papas"],
    "Producto": ["Hamburguesa Clásica", "Hamburguesa Doble", "Papas Fritas", "Papas Gajo"],
    "Cantidad": [10, 5, 20, 15],
    "Precio": [5.0, 7.5, 3.0, 4.0],
    "Fecha": pd.to_datetime(["2025-05-01", "2025-05-02", "2025-05-01", "2025-05-03"]),
}

df = pd.DataFrame(data)

# Crear GridOptionsBuilder
gb = GridOptionsBuilder.from_dataframe(df)

# Configurar para agrupar por 'Categoria' y ocultar esa columna (se usa solo para grupo)
gb.configure_column("Categoria", rowGroup=True, hide=True)

# Configurar columnas para que 'Producto' no se agrupe
gb.configure_column("Producto", rowGroup=False)

# Configurar estilo condicional para 'Cantidad' (color semáforo)
cellsytle_jscode = """
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
"""
gb.configure_column("Cantidad", cellStyle=cellsytle_jscode)

gridOptions = gb.build()

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    theme="alpine",
    fit_columns_on_grid_load=True,
)

