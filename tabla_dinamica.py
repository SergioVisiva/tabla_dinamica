import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Datos dentro del código
data = [
    {"Categoria": "Hamburguesas", "Producto": "Hamburguesa clásica", "Cantidad": 5, "Precio": 20, "Fecha": "2025-05-30"},
    {"Categoria": "Hamburguesas", "Producto": "Hamburguesa doble", "Cantidad": 15, "Precio": 35, "Fecha": "2025-05-29"},
    {"Categoria": "Papas", "Producto": "Papas fritas", "Cantidad": 25, "Precio": 10, "Fecha": "2025-05-28"},
    {"Categoria": "Papas", "Producto": "Papas a la francesa", "Cantidad": 8, "Precio": 12, "Fecha": "2025-05-27"},
]

df = pd.DataFrame(data)

# Agregar columna con emoji para la fecha para visual rápido
def emoji_fecha(fecha_str):
    from datetime import datetime, timedelta
    fecha = datetime.strptime(fecha_str, "%Y-%m-%d")
    hoy = datetime.now()
    delta = (hoy - fecha).days
    if delta <= 1:
        return "🟢 " + fecha_str  # reciente
    elif delta <= 3:
        return "🟡 " + fecha_str  # medio reciente
    else:
        return "🔴 " + fecha_str  # viejo

df["FechaVisual"] = df["Fecha"].apply(emoji_fecha)

# Construir opciones de grilla con jerarquía por Categoria y Producto
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("Categoria", rowGroup=True, hide=True)  # Grupo jerárquico
gb.configure_column("Producto", rowGroup=True, hide=True)
gb.configure_column("Cantidad", header_name="Cantidad",
                    cellStyle=lambda params: {
                        'backgroundColor': ('#ffcccc' if params['value'] < 10 else '#fff5cc' if params['value'] < 20 else '#ccffcc'),
                        'color': 'black'
                    })
gb.configure_column("Precio")
gb.configure_column("FechaVisual", header_name="Fecha")

gridOptions = gb.build()

# Mostrar tabla con st_aggrid
AgGrid(df, gridOptions=gridOptions, enable_enterprise_modules=True, theme="alpine", fit_columns_on_grid_load=True)
