import streamlit as st
import pandas as pd

# Simulación de datos
data = {
    "Fecha": ["2024-06-01", "2024-06-02", "2024-06-03", "2024-06-04"],
    "Categoría": ["Hamburguesas", "Papas", "Bebidas", "Hamburguesas"],
    "Producto": ["Clásica", "Fritas", "Coca-Cola", "Doble carne"],
    "Cantidad": [5, 15, 25, 8],
    "Precio": [15.0, 8.0, 5.0, 20.0]
}
df = pd.DataFrame(data)

st.title("Tabla con filtros y resaltado de columna 'Cantidad'")

# --- Filtros ---
categorias = st.multiselect("Filtrar por Categoría", options=df["Categoría"].unique(), default=df["Categoría"].unique())
producto = st.text_input("Buscar Producto")

df_filtrado = df[df["Categoría"].isin(categorias)]
if producto:
    df_filtrado = df_filtrado[df_filtrado["Producto"].str.contains(producto, case=False)]

# --- Aplicar color a la columna Cantidad ---
def resaltar_cantidad(val):
    if val < 10:
        color = 'background-color: red; color: white'
    elif val < 20:
        color = 'background-color: yellow; color: black'
    else:
        color = 'background-color: green; color: white'
    return color

styled_df = df_filtrado.style.applymap(resaltar_cantidad, subset=["Cantidad"])

# --- Mostrar tabla ---
st.dataframe(styled_df, use_container_width=True)


