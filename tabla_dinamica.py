import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Tabla Dinámica", layout="wide")

# Datos con la nueva columna "Categoría"
data = {
    "Producto": ["Hamburguesa", "Hamburguesa", "Papas", "Refresco", "Papas", "Refresco"],
    "Cantidad": [10, 5, 20, 15, 10, 5],
    "Precio_Unitario": [12, 12, 5, 3, 5, 3],
    "Vendedor": ["Luis", "Ana", "Luis", "Ana", "Luis", "Luis"],
    "Fecha": ["2024-05-01", "2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"],
    "Categoría": ["Comida", "Comida", "Comida", "Bebida", "Comida", "Bebida"]
}

df = pd.DataFrame(data)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

# Configuración de tabla dinámica
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)
gb.configure_column("Categoría", rowGroup=True, hide=True)  # Agrupa por Categoría
gb.configure_side_bar()  # Barra lateral para filtrar, agrupar, etc.
gb.configure_selection('single')

gridOptions = gb.build()

# Render de la app
st.title("Tabla Dinámica Estilo Excel")
st.markdown("Agrupa por categoría de comida para analizar ventas de hamburguesas, papas, bebidas, etc.")

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=500,
    theme="alpine"
)


