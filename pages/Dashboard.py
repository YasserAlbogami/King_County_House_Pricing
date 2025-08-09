import streamlit as st
import pandas as pd
from tabs import (
    general_insights,
    numrecial_analysis,
    geospatial_visualizations,
)


#  Page title
st.set_page_config(page_title="🏡 King County House Sales Dashboard", layout="wide")
st.title("🏡 King County House Sales Dashboard")

# Get filtered dataframe
df_filtered = pd.read_csv("data/kc_house_data.csv")


# Create tabs
tab0, tab1, tab2 = st.tabs([
    "📊 General Insights",
    "🌍 Numerical Analysis",
    "🗺️ Geospatial Visualizations",
])

# Render each tab content
with tab0:
    general_insights.render(df_filtered)

with tab1:
    numrecial_analysis.render(df_filtered)

with tab2:
    geospatial_visualizations.render(df_filtered)

