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

st.title("📊 Tabla Dinámica - Vista fija")

# Tabla dinámica fija con índices y columnas definidos
pivot = pd.pivot_table(
    df,
    index=['Categoría'],        # filas fijas
    columns=['Subcategoría'],   # columnas fijas
    values='Ventas',            # valor fijo
    aggfunc='sum',
    fill_value=0
)

st.write("Ventas por Categoría y Subcategoría:")
st.dataframe(pivot, use_container_width=True)

