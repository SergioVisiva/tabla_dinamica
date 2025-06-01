import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Datos de ejemplo con columna Cantidad
data = {
    "Categoria": ["Hamburguesas", "Hamburguesas", "Papas", "Papas"],
    "Producto": ["Leos Burger", "Cheese Burger", "Papas Fritas", "Papas Gajo"],
    "Cantidad": [3, 8, 12, 4],
    "Precio": [25, 30, 15, 18],
    "Fecha": pd.to_datetime(["2024-01-01", "2024-01-05", "2024-02-01", "2023-12-25"])
}

df = pd.DataFrame(data)

# Construir opciones de grilla
gb = GridOptionsBuilder.from_dataframe(df)

# Estilos condicionales solo para columna Cantidad
# Rojo si Cantidad < 5
gb.configure_column(
    "Cantidad",
    cellStyle={
        'if': {'filter': 'Cantidad < 5'}, 'backgroundColor': 'red', 'color': 'white'
    }
)
# Amarillo si 5 <= Cantidad < 10
gb.configure_column(
    "Cantidad",
    cellStyle={
        'if': {'filter': 'Cantidad >= 5 && Cantidad < 10'}, 'backgroundColor': 'yellow', 'color': 'black'
    }
)
# Verde si Cantidad >= 10
gb.configure_column(
    "Cantidad",
    cellStyle={
        'if': {'filter': 'Cantidad >= 10'}, 'backgroundColor': 'green', 'color': 'white'
    }
)

gridOptions = gb.build()

st.title("Tabla dinámica con color semáforo en Cantidad")

AgGrid(df, gridOptions=gridOptions, theme="alpine", fit_columns_on_grid_load=True)

