from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

data = {
    "categoria": ["Hamburguesa", "Hamburguesa", "Papas", "Papas"],
    "producto": ["Cheese", "Bacon", "Clasicas", "Con queso"],
    "cantidad": [10, 3, 15, 0],
    "precio": [25, 30, 10, 12],
    "fecha": ["2025-05-30", "2025-05-31", "", None]
}

df = pd.DataFrame(data)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True)
gb.configure_column("categoria", rowGroup=True, hide=True)
gb.configure_column("producto", rowGroup=True, hide=True)

# Colores sin funciones lambda, usando estilos estáticos para probar
gb.configure_column("cantidad", cellStyle={'color': 'white', 'backgroundColor': 'green'})
gb.configure_column("precio", cellStyle={'color': 'white', 'backgroundColor': 'orange'})

gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, theme="alpine", fit_columns_on_grid_load=True)
