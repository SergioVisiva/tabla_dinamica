import streamlit as st
import pandas as pd

# Datos de ejemplo
data = {
    'Categoría': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Subcategoría': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'Ventas': [100, 150, 200, 250, 300, 350],
    'Cantidad': [10, 15, 20, 25, 30, 35]
}

df = pd.DataFrame(data)

st.set_page_config(page_title="Tabla Dinámica", layout="wide")
st.title("📊 Ejemplo de Tabla Dinámica con Streamlit")

rows = st.multiselect('Selecciona columnas para filas', df.columns.tolist(), default=['Categoría'])
cols = st.multiselect('Selecciona columnas para columnas', df.columns.tolist(), default=['Subcategoría'])
vals = st.selectbox('Selecciona la columna de valores', ['Ventas', 'Cantidad'])

if rows and cols:
    pivot = pd.pivot_table(df, index=rows, columns=cols, values=vals, aggfunc='sum', fill_value=0)
    st.subheader("Resultado de la tabla dinámica:")
    st.dataframe(pivot, use_container_width=True)
else:
    st.warning("Por favor selecciona al menos una columna para filas y columnas.")
