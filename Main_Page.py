import streamlit as st
from main_tabs import (
    dataset_overview,
    preprocessing,
)
import pandas as pd
# Apply global style and logo


# Set page config
st.set_page_config(page_title="🧪 Project Overview", layout="wide")


df_filtered = pd.read_csv("data/kc_house_data.csv")

# ---- Main Content ----
st.title("🏡 King County House Sales Project Overview")
st.markdown(
    "A quick walkthrough of the motivation, data, and preprocessing steps behind the project.")

if st.button("📈 Open Dashboard"):
    st.switch_page("pages/Dashboard.py")

# Tabs
tab1, tab2, tab3 = st.tabs([
    "📌 The Project",
    "📊 Dataset Overview",
    "🛠️ Preprocessing and Cleaning"
])


with tab1:
    st.markdown("""
## 🏡 Introduction to the King County House Sales Dataset

### 📄 Overview
This dataset contains **house sales records from King County, USA**, including Seattle, for the period **May 2014 to May 2015**.  
It’s widely used for **real estate market analysis** and **price prediction** tasks.

---

### 📊 What's Inside the Dataset?
The dataset has **21 features** capturing details such as:
- 📅 **Sale date**  
- 💰 **Price** of the property  
- 📏 **Living area size** (`sqft_living`)  
- 🛏️ **Bedrooms** and 🛁 **Bathrooms**  
- 📐 **Lot size** (`sqft_lot`)  
- 🏠 **Floors**, **waterfront** status, and view quality  
- 📍 **Location details** (`zipcode`, latitude, longitude)  
- 🏗️ **Year built** and **renovation year**  
- Overall **condition** and **grade** of the property

---

### 🎯 Why This Dataset?
Real estate pricing depends on multiple factors — location, property size, condition, and even the view.  
Analyzing this dataset allows us to:
- Understand **price-driving factors** 🧮  
- Compare trends across **neighborhoods** 🌍  
- Identify **seasonal patterns** 📈  
- Build **predictive models** for price estimation 🤖  

---

### 💡 Project Goals
1. Perform **Exploratory Data Analysis (EDA)** to spot patterns and trends.  
2. Investigate **feature relationships** affecting housing prices.  
3. Develop **machine learning models** to predict prices from property characteristics.  
4. Provide insights that could help buyers, sellers, and urban planners.  
""")

    # Path from root

with tab2:
   dataset_overview.render(df_filtered)

with tab3:
    
    preprocessing.render(df_filtered)

# ---- Optional main page button ----
st.markdown("---")
