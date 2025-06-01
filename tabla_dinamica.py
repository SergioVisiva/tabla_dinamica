import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Datos
data = [
    {"Categoria": "Hamburguesas", "Producto": "Hamburguesa clásica", "Cantidad": 5, "Precio": 20, "Fecha": "2025-05-30"},
    {"Categoria": "Hamburguesas", "Producto": "Hamburguesa doble", "Cantidad": 15, "Precio": 35, "Fecha": "2025-05-29"},
    {"Categoria": "Papas", "Producto": "Papas fritas", "Cantidad": 25, "Precio": 10, "Fecha": "2025-05-28"},
    {"Categoria": "Papas", "Producto": "Papas a la francesa", "Cantidad": 8, "Precio": 12, "Fecha": "2025-05-27"},
]

df = pd.DataFrame(data)

# Configuración simple de AgGrid mostrando solo Cantidad agrupada por Categoría
gb = GridOptionsBuilder.from_dataframe(df[['Categoria', 'Cantidad']])
gb.configure_column("Categoria", rowGroup=True, hide=False)  # Agrupar por categoría y mostrarla
gb.configure_column("Cantidad", aggFunc='sum')  # Mostrar suma de cantidades por categoría

gridOptions = gb.build()

# Mostrar tabla
st.header("Cantidades por Categoría")
AgGrid(
    df,
    gridOptions=gridOptions,
    enable_enterprise_modules=True,
    theme="alpine",
    height=300
)
