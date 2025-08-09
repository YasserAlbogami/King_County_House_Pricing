import streamlit as st
import plotly.express as px
import pandas as pd

def render(df_filtered):
    """Render stacked histogram of Life Expectancy by Development Status."""    
    
    # ---- General Insights ----
    st.subheader("📊 General Insights")

    col1, col2, col3 = st.columns(3)

    # Avg condition rating
    col1.metric("🏚️ Avg. Condition", f"{df_filtered['condition'].mean():.1f} / 5")

    # % Waterfront homes
    waterfront_share = (df_filtered['waterfront'] == 1).mean() * 100
    col2.metric("🌊 Waterfront Homes", f"{waterfront_share:.1f}%")

    # Avg Grade
    col3.metric("🏗️ Avg. Grade", f"{df_filtered['grade'].mean():.1f} / 13")

    
    # 1

    st.subheader("1: 📊 Price Distribution by Lot Size Category")

    bins = [0, 2000, 4000, 6000, 10000, 20000, df_filtered['sqft_lot'].max()]
    labels = ['<2k', '2k–4k', '4k–6k', '6k–10k', '10k–20k', '20k+']

    df_filtered['lot_size_range'] = pd.cut(df_filtered['sqft_lot'], bins=bins, labels=labels)
    lot_avg = df_filtered.groupby('lot_size_range')['price'].mean().reset_index()

    fig = px.bar(
        lot_avg,
        x='lot_size_range',
        y='price',
        color='price',
        color_continuous_scale='Blues',
        text='price',
        title='Avg Price by Lot Size Category'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)

    # 2

    st.subheader("2: 📈 Sqft Living vs. Price by Grade")

    fig = px.scatter(
        df_filtered,
        x='sqft_living',
        y='price',
        color='grade',
        color_continuous_scale='Blues',
        hover_data=['bedrooms', 'bathrooms', 'zipcode'],
        title='Sqft Living vs. Price'
    )
    st.plotly_chart(fig, use_container_width=True)


    # 3

    st.subheader("3: 🏞️ Avg Price by View Quality")

    view_avg = df_filtered.groupby('view')['price'].mean().reset_index()

    fig = px.bar(
        view_avg,
        x='view',
        y='price',
        color='price',
        color_continuous_scale='Blues',
        text='price',
        title='Avg Price by View Quality'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


    # 4

    st.subheader("4: 🏚️ Average Price by Condition")

    cond_avg = df_filtered.groupby('condition')['price'].mean().reset_index()

    fig = px.bar(
        cond_avg,
        x='condition',
        y='price',
        color='price',
        color_continuous_scale='Blues',
        text='price',
        title='Average Price by Condition'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    st.plotly_chart(fig, use_container_width=True)


    # 5

    st.subheader("5: 🛠️ Avg Price — Renovated vs Not Renovated")

    df_filtered['was_renovated'] = df_filtered['yr_renovated'].apply(lambda x: 'Yes' if x > 0 else 'No')

    fig = px.histogram(
        df_filtered,
        x='was_renovated',
        y='price',
        histfunc='avg',
        color='was_renovated',
        title='Avg Price: Renovated vs Not Renovated'
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)
