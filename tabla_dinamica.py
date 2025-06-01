from st_aggrid import AgGrid, GridOptionsBuilder
import pandas as pd
import streamlit as st

data = {
    "categoria": ["Hamburguesa", "Hamburguesa", "Papas", "Papas"],
    "producto": ["Cheese", "Bacon", "Clasicas", "Con queso"],
    "cantidad": [10, 3, 15, 0],
    "precio": [25, 30, 10, 12],
    "fecha": ["2025-05-30", "2025-05-31", "", None]  # <-- Aquí hay fechas vacías o None
}

df = pd.DataFrame(data)

gb = GridOptionsBuilder.from_dataframe(df)
gb.configure_default_column(groupable=True)

# Columna categoría como grupo principal y producto debajo como subgrupo
gb.configure_column("categoria", rowGroup=True, hide=True)
gb.configure_column("producto", rowGroup=True, hide=True)

# Columna cantidad con semáforo de color
gb.configure_column(
    "cantidad",
    cellStyle=lambda params: {
        "color": "white",
        "backgroundColor": "green" if params.value > 5 else "orange" if params.value > 0 else "red"
    }
)

# Columna precio con semáforo de color
gb.configure_column(
    "precio",
    cellStyle=lambda params: {
        "color": "white",
        "backgroundColor": "green" if params.value > 20 else "orange" if params.value > 10 else "red"
    }
)

# Columna fecha con icono solo si hay valor y si termina en "-31" muestra un icono (ejemplo)
gb.configure_column(
    "fecha",
    cellRenderer="""
    function(params) {
        if (!params.value) {
            return "";
        }
        let icon = params.value.endsWith("-31") ? "📅" : "📆";
        return icon + " " + params.value;
    }
    """
)

gridOptions = gb.build()

AgGrid(df, gridOptions=gridOptions, enableEnterpriseModules=True, theme="alpine", fit_columns_on_grid_load=True)

