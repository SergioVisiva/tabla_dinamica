import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Tabla Dinámica", layout="wide")

# Datos incluidos directamente en el código
data = {
    "Producto": ["Hamburguesa", "Hamburguesa", "Papas", "Refresco", "Papas", "Refresco"],
    "Cantidad": [10, 5, 20, 15, 10, 5],
    "Precio_Unitario": [12, 12, 5, 3, 5, 3],
    "Vendedor": ["Luis", "Ana", "Luis", "Ana", "Luis", "Luis"],
    "Fecha": ["2024-05-01", "2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"]
}

df = pd.DataFrame(data)
df["Fecha"] = pd.to_datetime(df["Fecha"])

# Calcular columna de ingreso total
df["Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

# Crear configuración de la tabla
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
gb.configure_side_bar()  # Barra lateral para agrupar, filtrar, etc.
gb.configure_selection('single')

# Construir opciones
gridOptions = gb.build()

# Mostrar tabla
st.title("Tabla Dinámica Estilo Excel")
st.markdown("Agrupa, ordena y analiza los datos como en una tabla dinámica.")

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=450,
    theme="alpine"
)

