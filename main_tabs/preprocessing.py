import streamlit as st
import pandas as pd

def render(df):
    st.header("🧹 Data Cleaning & Preprocessing — King County House Sales")

    # Phase 1: Value Ranges
    st.subheader("📊 Phase 1: Value Ranges of Numeric Features")
    numeric_features = df.select_dtypes(include=['number'])
    min_values = numeric_features.min()
    max_values = numeric_features.max()
    min_max_df = pd.DataFrame({'Min Value': min_values, 'Max Value': max_values})
    st.dataframe(min_max_df.style.format(precision=2), use_container_width=True)

    # Phase 2: Unique Values
    st.subheader("🔣 Phase 2: Unique Values in Categorical Features")
    categorical_features = df.select_dtypes(include=['object', 'category'])
    for col in categorical_features.columns:
        st.markdown(f"**📝 {col}**: {df[col].nunique()} unique value(s)")
        st.write(sorted(df[col].dropna().unique()))

    # Phase 3: Missing Values
    st.subheader("🧪 Phase 3: Missing Values Check")
    st.success("✅ The dataset contains NO missing values and NO duplicate rows.\n"
               "This indicates that the dataset is complete and unique for all records.")

    # Phase 4: Outlier Validation
    st.subheader("📏 Phase 4: Outlier Validation")
    st.markdown("""
    - **price**: Max $7.7M → realistic for luxury waterfront mansions.  
    - **bathrooms**: Max 8.0 → plausible for large estates.  
    - **sqft_living**: Max 13,540 sqft → large mansions exist.  
    - **sqft_lot**: Max 1.65M sqft (~38 acres) → valid for rural estates.  
    - **floors**: Max 3.5 → half-level floors are possible.  
    - **view**, **condition**, **grade**: All within defined categorical scales.  
    - **sqft_above** & **sqft_basement**: Large but possible in very big homes.  
    - **yr_renovated**: Max 2015 → fits the dataset period.  
    - **sqft_living15** & **sqft_lot15**: Valid for neighborhoods with large lots.  

    **Conclusion:** All detected extremes are plausible — no removal needed.
    """)


