import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Datos con valores sin NaN ni None
data = {
    "categoria": ["Hamburguesa", "Hamburguesa", "Papas", "Papas"],
    "producto": ["Cheese", "Bacon", "Clasicas", "Con queso"],
    "cantidad": [10, 3, 15, 0],
    "precio": [25, 30, 10, 12],
    "fecha": ["2025-05-30", "2025-05-31", "", ""]
}

df = pd.DataFrame(data)

# Reemplaza NaN o None con ''
df = df.fillna('')

# Icono en fecha (solo string)
def icono_fecha(fecha):
    if fecha == '' or fecha is None:
        return ''
    if fecha.endswith("-31"):
        return "📅 " + fecha
    else:
        return "📆 " + fecha

df['fecha_icono'] = df['fecha'].apply(icono_fecha)

# Estilos de celdas, solo diccionarios planos
def style_cantidad(params):
    val = params.value
    if val == '' or val is None:
        return {}
    if val > 5:
        return {'color': 'white', 'backgroundColor': 'green'}
    elif val > 0:
        return {'color': 'white', 'backgroundColor': 'orange'}
    else:
        return {'color': 'white', 'backgroundColor': 'red'}

def style_precio(params):
    val = params.value
    if val == '' or val is None:
        return {}
    if val > 20:
        return {'color': 'white', 'backgroundColor': 'green'}
    elif val > 10:
        return {'color': 'white', 'backgroundColor': 'orange'}
    else:
        return {'color': 'white', 'backgroundColor': 'red'}

# Construye grid options
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_column("categoria", rowGroup=True, hide=True)
gb.configure_column("producto", rowGroup=True, hide=True)
gb.configure_column("cantidad", cellStyle=style_cantidad)
gb.configure_column("precio", cellStyle=style_precio)
gb.configure_column("fecha_icono", headerName="Fecha")

gridOptions = gb.build()

# DEBUG: verificar que gridOptions se puede convertir a JSON
import json
try:
    json.dumps(gridOptions)
except Exception as e:
    st.error(f"Error en gridOptions JSON: {e}")

AgGrid(
    df,
    gridOptions=gridOptions,
    theme="alpine",
    fit_columns_on_grid_load=True,
    enable_enterprise_modules=True
)

