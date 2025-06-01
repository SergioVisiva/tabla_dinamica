import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Tabla Dinámica", layout="wide")

# Datos embebidos directamente en el código
data = {
    "Producto": ["Hamburguesa", "Hamburguesa", "Papas", "Refresco", "Papas", "Refresco"],
    "Cantidad": [10, 5, 20, 15, 10, 5],
    "Precio_Unitario": [12, 12, 5, 3, 5, 3],
    "Vendedor": ["Luis", "Ana", "Luis", "Ana", "Luis", "Luis"],
    "Fecha": ["2024-05-01", "2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"]
}

df = pd.DataFrame(data)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Configurar opciones de tabla dinámica
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, enablePivot=True, enableValue=True, editable=False)
gb.configure_side_bar()
gb.configure_grid_options(pivotMode=True)

grid_options = gb.build()

# Mostrar la tabla dinámica
st.title("Tabla Dinámica Interactiva (Estilo Excel)")
AgGrid(
    df,
    gridOptions=grid_options,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=400
)

# Construir opciones de la tabla
go = gb.build()

# Mostrar la tabla en la aplicación
st.title("Tabla Dinámica Interactiva")
AgGrid(data, gridOptions=go, height=500, enable_enterprise_modules=True)
