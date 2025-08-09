import streamlit as st
import pandas as pd
from typing import Optional

def _parse_date(series: pd.Series) -> Optional[pd.Series]:
    try:
        return pd.to_datetime(series, errors="coerce")
    except Exception:
        return None

def render(df_filtered: pd.DataFrame):
    st.header("📌 Dataset Overview — King County House Sales (Seattle Area)")

    # Ensure typical kc_house columns exist
    expected_cols = {
        "price","zipcode","sqft_living","yr_built","date","bedrooms","bathrooms",
        "sqft_lot","floors","waterfront","view","condition","grade","sqft_above",
        "sqft_basement","yr_renovated","lat","long","sqft_living15","sqft_lot15","id"
    }
    available = set(df_filtered.columns.str.lower())
    # Create a case-insensitive accessor
    df = df_filtered.copy()
    df.columns = [c.lower() for c in df.columns]

    # ---- Top summary cards ----
    col1, col2, col3 = st.columns([1, 1, 1])

    # 1) Unique ZIP codes
    if "zipcode" in df.columns:
        num_zips = df["zipcode"].nunique()
        col1.metric("📮 Unique ZIP Codes", f"{num_zips}")
    else:
        col1.metric("📮 Unique ZIP Codes", "—")

    # 2) Average Price
    if "price" in df.columns:
        avg_price = df["price"].mean()
        col2.metric("💰 Avg. Price", f"${avg_price:,.0f}")
    else:
        col2.metric("💰 Avg. Price", "—")

    # 3) Median Living Area
    if "sqft_living" in df.columns:
        med_living = df["sqft_living"].median()
        col3.metric("📏 Median Living Area", f"{med_living:,.0f} sqft")
    else:
        col3.metric("📏 Median Living Area", "—")


    st.markdown("---")

    # ---- Date coverage (if available) ----
    st.subheader("🗓️ Coverage")
    if "date" in df.columns:
        date_series = _parse_date(df["date"])
        if date_series is not None and date_series.notna().any():
            st.markdown(
                f"- **Date Range**: `{date_series.min().date()}` → `{date_series.max().date()}`"
            )
        else:
            st.markdown("- **Date Range**: (unparseable date format)")
    else:
        st.markdown("- **Date Range**: (no `date` column)")

    # ---- Preview ----
    st.subheader("📂 Dataset Preview")
    preview_df = df_filtered.head(10).reset_index(drop=True)
    preview_df.index = preview_df.index + 1
    preview_df.index.name = "Row"
    st.dataframe(preview_df, use_container_width=True)

    # ---- Shape & dtypes ----
    st.subheader("📈 Shape & Data Types")
    st.markdown(f"- 🔢 **Rows**: `{df_filtered.shape[0]:,}`")
    st.markdown(f"- 📊 **Columns**: `{df_filtered.shape[1]}`")
    st.write(df_filtered.dtypes)

    # ---- Descriptive statistics (numeric only) ----
    st.subheader("📊 Descriptive Statistics (Numeric)")
    numeric_cols = df_filtered.select_dtypes(include="number")
    if not numeric_cols.empty:
        st.dataframe(numeric_cols.describe().T.style.format(precision=2), use_container_width=True)
    else:
        st.info("No numeric columns found for descriptive statistics.")

    st.markdown("---")

    # ---- Column descriptions for kc_house_data ----
    st.markdown("""
## 🧾 Column Descriptions (King County House Sales)

| Column            | Description |
|-------------------|-------------|
| `id`              | Unique identifier for the sale/listing. |
| `date`            | Date of the sale (typically between May 2014 and May 2015). |
| `price`           | Sale price of the home (USD). |
| `bedrooms`        | Number of bedrooms. |
| `bathrooms`       | Number of bathrooms (can be fractional, e.g., 2.5). |
| `sqft_living`     | Interior living space (square feet). |
| `sqft_lot`        | Lot size (square feet). |
| `floors`          | Number of floors (levels) in the house. |
| `waterfront`      | Binary indicator (1 = waterfront, 0 = not). |
| `view`            | Index for quality of the view (higher = better). |
| `condition`       | Overall condition rating (1–5). |
| `grade`           | Overall grade (1–13), combining design & construction quality. |
| `sqft_above`      | Square footage above ground. |
| `sqft_basement`   | Square footage of the basement (0 if none). |
| `yr_built`        | Year the house was originally built. |
| `yr_renovated`    | Year of last renovation (0 if never renovated). |
| `zipcode`         | Postal ZIP code. |
| `lat`             | Latitude coordinate. |
| `long`            | Longitude coordinate. |
| `sqft_living15`   | Living area (sqft) of the 15 nearest neighbors. |
| `sqft_lot15`      | Lot size (sqft) of the 15 nearest neighbors. |

**Objective of this project:** explore pricing drivers, location effects, and property characteristics, and build predictive models for house prices in the Seattle (King County) market.
""")
