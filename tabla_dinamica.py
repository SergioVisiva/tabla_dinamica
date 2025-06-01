import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

st.set_page_config(page_title="Tabla Dinámica", layout="wide")

# Datos de ejemplo con categoría y producto
data = {
    "Categoría": ["Comida", "Comida", "Comida", "Bebida", "Comida", "Bebida"],
    "Producto": ["Hamburguesa", "Hamburguesa", "Papas", "Refresco", "Papas", "Refresco"],
    "Cantidad": [10, 5, 20, 15, 10, 5],
    "Precio_Unitario": [12, 12, 5, 3, 5, 3],
    "Vendedor": ["Luis", "Ana", "Luis", "Ana", "Luis", "Luis"],
    "Fecha": ["2024-05-01", "2024-05-01", "2024-05-02", "2024-05-02", "2024-05-03", "2024-05-03"]
}

df = pd.DataFrame(data)
df["Fecha"] = pd.to_datetime(df["Fecha"])
df["Total_Venta"] = df["Cantidad"] * df["Precio_Unitario"]

# Configuración de la tabla dinámica con jerarquía Categoría > Producto
gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True, value=True, enableRowGroup=True, aggFunc='sum', editable=False)

# Agrupar por Categoría y Producto en jerarquía
gb.configure_column("Categoría", rowGroup=True, hide=True)
gb.configure_column("Producto", rowGroup=True, hide=True)

gb.configure_side_bar()  # Barra lateral para filtros y control
gb.configure_selection('single')

gridOptions = gb.build()

# Render de la app
st.title("Tabla Dinámica por Categoría y Producto")
st.markdown("Expande cada categoría para ver los productos dentro de ella, como en una tabla dinámica jerárquica de Excel.")

AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    fit_columns_on_grid_load=True,
    height=500,
    theme="alpine"
)

