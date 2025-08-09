# tabs/project_info.py
import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

def render(df_filtered):
    
    st.header("🗺️ Geospatial Visualizations")


        # Group by zipcode and calculate average condition + lat/long
    zip_condition = df_filtered.groupby('zipcode').agg({
        'lat': 'mean',
        'long': 'mean',
        'condition': 'mean'
    }).reset_index().rename(columns={'condition': 'avg_condition'})

    # Create condition categories
    bins = [0, 1.5, 2.5, 3.5, 4.5, 5.1]
    labels = ['Poor', 'Fair', 'Average', 'Good', 'Excellent']
    zip_condition['condition_category'] = pd.cut(
        zip_condition['avg_condition'],
        bins=bins,
        labels=labels,
        include_lowest=True
    )

    # 1
    fig_condition = px.scatter_mapbox(
        zip_condition,
        lat="lat",
        lon="long",
        size="avg_condition",
        color="condition_category",
        hover_name="zipcode",
        hover_data={"avg_condition": True, "condition_category": True},
        color_discrete_sequence=px.colors.qualitative.Set2,
        size_max=15,
        zoom=9,
        mapbox_style="carto-positron",
    )

    # Adjust map size
    fig_condition.update_layout(
        width=1200,
        height=700
    )
    st.subheader("1: 🗺️ Map of Binned Average House Condition by Zipcode")
    st.plotly_chart(fig_condition, use_container_width=False)



    # 2
    st.subheader("2: 🗺️ Map of House Conditions")



    # Create geometry points
    geometry = [Point(xy) for xy in zip(df_filtered['long'], df_filtered['lat'])]
    geo_df = gpd.GeoDataFrame(df_filtered, geometry=geometry)
    geo_df.set_crs(epsg=4326, inplace=True)

    # Extract lat/lon for Plotly
    geo_df_px = geo_df.copy()
    geo_df_px['lon'] = geo_df_px.geometry.x
    geo_df_px['lat'] = geo_df_px.geometry.y

    # Plot
    fig = px.scatter_mapbox(
        geo_df_px,
        lat="lat",
        lon="lon",
        color="condition",
        color_continuous_scale="Viridis",
        size_max=8,
        zoom=9,
        mapbox_style="carto-positron",
        title="Map of House Conditions"
    )

    # Adjust map size
    fig.update_layout(
        width=1200,
        height=700
    )

    st.plotly_chart(fig, use_container_width=False)


