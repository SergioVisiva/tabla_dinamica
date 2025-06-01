import streamlit as st
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder

# Cargar datos desde un archivo CSV
@st.cache_data()
def load_data():
    data = pd.read_csv("data.csv", parse_dates=["referenceDate"])
    return data

data = load_data()

# Configurar opciones de la tabla
gb = GridOptionsBuilder.from_dataframe(data)

# Habilitar características por defecto
gb.configure_default_column(
    resizable=True,
    filterable=True,
    sortable=True,
    editable=False,
    groupable=True
)

# Configurar columnas específicas
gb.configure_column("state", header_name="State", width=80)
gb.configure_column("powerPlant", header_name="Power Plant", flex=1, tooltipField="powerPlant")
gb.configure_column("recordType", header_name="Record Type", width=110)
gb.configure_column("buyer", header_name="Buyer", width=150, tooltipField="buyer")
gb.configure_column(
    "referenceDate",
    header_name="Reference Date",
    width=100,
    valueFormatter="value != undefined ? new Date(value).toLocaleString('en-US', {dateStyle:'medium'}): ''",
    pivot=True
)
gb.configure_column(
    "hoursInMonth",
    header_name="Hours in Month",
    width=50,
    type=["numericColumn"]
)
gb.configure_column(
    "volumeMWh",
    header_name="Volume [MWh]",
    width=100,
    type=["numericColumn"],
    valueFormatter="value.toLocaleString()",
    aggFunc="sum"
)

# Habilitar modo de pivoteo
gb.configure_grid_options(pivotMode=True)

# Construir opciones de la tabla
go = gb.build()

# Mostrar la tabla en la aplicación
st.title("Tabla Dinámica Interactiva")
AgGrid(data, gridOptions=go, height=500, enable_enterprise_modules=True)
