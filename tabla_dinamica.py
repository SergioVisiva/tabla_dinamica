from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

# Datos
data = {
    "categoria": ["Hamburguesa", "Hamburguesa", "Papas", "Papas"],
    "producto": ["Cheese", "Bacon", "Clasicas", "Con queso"],
    "cantidad": [10, 3, 15, 0],
    "precio": [25, 30, 10, 12],
    "fecha": ["2025-05-30", "2025-05-31", "", None]
}

df = pd.DataFrame(data)

# Funciones para estilos condicionales
def style_cantidad(params):
    val = params.value
    if val is None or val == '':
        return {}
    if val > 5:
        return {'color': 'white', 'backgroundColor': 'green'}
    elif val > 0:
        return {'color': 'white', 'backgroundColor': 'orange'}
    else:
        return {'color': 'white', 'backgroundColor': 'red'}

def style_precio(params):
    val = params.value
    if val is None or val == '':
        return {}
    if val > 20:
        return {'color': 'white', 'backgroundColor': 'green'}
    elif val > 10:
        return {'color': 'white', 'backgroundColor': 'orange'}
    else:
        return {'color': 'white', 'backgroundColor': 'red'}

def icono_fecha(fecha):
    if not fecha or pd.isna(fecha) or fecha == '':
        return ''
    if fecha.endswith("-31"):
        return "📅 " + fecha
    else:
        return "📆 " + fecha

# Nueva columna para mostrar la fecha con ícono
df['fecha_icono'] = df['fecha'].apply(icono_fecha)

# Construcción del GridOptionsBuilder
gb = GridOptionsBuilder.from_dataframe(df)

# Configurar columnas para agrupación (jerarquía)
gb.configure_column("categoria", rowGroup=True, hide=True)
gb.configure_column("producto", rowGroup=True, hide=True)

# Columnas que tendrán color (no en rowGroup)
gb.configure_column("cantidad", cellStyle=style_cantidad)
gb.configure_column("precio", cellStyle=style_precio)

# Mostrar columna de fecha con icono, sin ocultar, sin agrupación
gb.configure_column("fecha_icono", headerName="Fecha", suppressSizeToFit=False)

# Construir opciones
gridOptions = gb.build()

# Mostrar en Streamlit
AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    theme="alpine",
    fit_columns_on_grid_load=True,
)
