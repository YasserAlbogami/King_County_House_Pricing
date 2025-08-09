# tabs/numerical_analysis.py
import streamlit as st
import plotly.express as px
import pandas as pd


def render(df_filtered):
    st.header("🌍 Numerical Analysis")

    # Create 'age_of_house' column
    df_filtered['age_of_house'] = df_filtered['yr_built'].max() - df_filtered['yr_built']

    col1, col2, col3 = st.columns(3)

    # 1) Average Age of House
    avg_age = df_filtered['age_of_house'].mean()
    col1.metric("🏗️ Average House Age", f"{avg_age:.1f} years")

    # 2) Number of Renovated Homes
    num_renovated = (df_filtered['yr_renovated'] > 0).sum()
    col2.metric("🛠️ Renovated Homes", f"{num_renovated:,}")

    # 3) Number of Non-Renovated Homes
    num_not_renovated = (df_filtered['yr_renovated'] == 0).sum()
    col3.metric("🏠 Non-Renovated Homes", f"{num_not_renovated:,}")


    # 1

    st.subheader("1: 🌊 Avg Price — Waterfront vs Non-Waterfront")

    df_filtered['waterfront_label'] = df_filtered['waterfront'].apply(lambda x: 'Yes' if x == 1 else 'No')

    fig = px.histogram(
        df_filtered,
        x='waterfront_label',
        y='price',
        histfunc='avg',
        color='waterfront_label',
        title='Avg Price: Waterfront vs Non-Waterfront'
    )

    fig.update_layout(showlegend=False)
    st.plotly_chart(fig, use_container_width=True)


    # 2

    st.subheader("2: 🔍 Correlation Heatmap (Numerical Features)")

    # Compute correlation matrix
    corr = df_filtered.corr(numeric_only=True)

    # Create heatmap
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="Blues",
        title="Correlation Heatmap"
    )
    fig.update_layout(
        xaxis_title="Features",
        yaxis_title="Features",
        width=800,
        height=800
    )

    st.plotly_chart(fig, use_container_width=True)

    # --- Subset correlation heatmap ---
    st.markdown("**Subset: Condition, Grade, View, Waterfront**")

    selected_cols = ['condition', 'grade', 'view', 'waterfront']
    subset_corr = df_filtered[selected_cols].corr()

    fig_subset = px.imshow(
        subset_corr,
        text_auto=".2f",
        color_continuous_scale="YlGnBu",
        title="Correlation Heatmap (Selected Features)"
    )
    fig_subset.update_layout(
        xaxis_title="Features",
        yaxis_title="Features",
        width=500,
        height=500
    )
    st.plotly_chart(fig_subset, use_container_width=True)


    # 3
    st.subheader("3: 🏢 Average Price by Number of Floors")

    # Round up floors
    floor_avg = df_filtered.copy()
    floor_avg['floors'] = floor_avg['floors'].apply(lambda x: int(x) if x.is_integer() else int(x) + 1)

    # Group and calculate average price
    floor_avg = floor_avg.groupby('floors')['price'].mean().reset_index()

    fig = px.bar(
        floor_avg,
        x='floors',
        y='price',
        color='price',
        color_continuous_scale='Blues',
        text='price',
        title='Average Price by Number of Floors'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')
    
    # Make x-axis discrete (category type) without converting to string
    fig.update_xaxes(type='category')   
    st.plotly_chart(fig, use_container_width=True)

        
    

    # 4

    st.subheader("4: 🛏️ Average Price by Number of Bedrooms")

    bed_avg = df_filtered.groupby('bedrooms')['price'].mean().reset_index()

    fig = px.bar(
        bed_avg,
        x='bedrooms',
        y='price',
        color='price',
        color_continuous_scale='Blues',
        text='price',
        title='Average Price by Number of Bedrooms'
    )
    fig.update_traces(texttemplate='$%{text:,.0f}', textposition='outside')

    # Make x-axis discrete
    fig.update_xaxes(type='category')

    st.plotly_chart(fig, use_container_width=True)



    # 5
    st.subheader("5: 📅 Number of Sales by Month")

    # Extract month from date
    df_filtered['month'] = pd.to_datetime(df_filtered['date']).dt.month

    # Count sales per month
    monthly_sales = df_filtered['month'].value_counts().sort_index().reset_index()
    monthly_sales.columns = ['month', 'count']

    # Create line chart
    fig = px.line(
        monthly_sales,
        x='month',
        y='count',
        title='Number of Sales by Month',
        markers=True,
        color_discrete_sequence=['#1f77b4']
    )

    fig.update_layout(xaxis=dict(tickmode='linear'))
    st.plotly_chart(fig, use_container_width=True)
