import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Datos de ejemplo
data = {
    'Categoría': ['A', 'A', 'B', 'B', 'C', 'C'],
    'Subcategoría': ['X', 'Y', 'X', 'Y', 'X', 'Y'],
    'Ventas': [100, 150, 200, 250, 300, 350],
    'Cantidad': [10, 15, 20, 25, 30, 35]
}

df = pd.DataFrame(data)

st.title("Tabla Dinámica estilo Excel con Streamlit")

# Construir opciones de la grilla con agrupación
gb = GridOptionsBuilder.from_dataframe(df)

# Indicar las columnas que serán agrupadas (las jerarquías)
gb.configure_column("Categoría", rowGroup=True, hide=True)
gb.configure_column("Subcategoría", rowGroup=True, hide=True)

# La columna con valores que queremos sumar o mostrar
gb.configure_aggregation("Ventas", aggFunc='sum')
gb.configure_aggregation("Cantidad", aggFunc='sum')

# Habilitar expansión y agrupación automática
gb.configure_grid_options(autoGroupColumnDef={'headerName': 'Jerarquía', 'cellRenderer': 'agGroupCellRenderer'})

grid_options = gb.build()

# Mostrar la tabla con AgGrid y opciones configuradas
AgGrid(df, gridOptions=grid_options, enableEnterpriseModules=True, fit_columns_on_grid_load=True)

st.write("Puedes expandir y colapsar las categorías y subcategorías para ver la jerarquía.")


