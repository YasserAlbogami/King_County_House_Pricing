import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler, PolynomialFeatures
from sklearn.model_selection import train_test_split
from sklearn.linear_model import Ridge
from sklearn.metrics import r2_score

# ---------------------------
# Cache data and model training
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("data/kc_house_data.csv")
    df["age_of_house"] = df['yr_built'].max() - df['yr_built']
    return df

@st.cache_resource
def train_model(df):
    drop_cols = [c for c in ["id", "date", "price", "yr_built"] if c in df.columns]
    X = df.drop(columns=drop_cols)
    y = df["price"]

    if "zipcode" in X.columns:
        X = pd.get_dummies(X, columns=["zipcode"], drop_first=True)

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    poly = PolynomialFeatures(degree=2, include_bias=True)
    X_poly = poly.fit_transform(X_scaled)

    X_train, X_test, y_train, y_test = train_test_split(
        X_poly, y, test_size=0.2, random_state=42
    )

    lr = Ridge(alpha=10.0, random_state=42, max_iter=5000)
    lr.fit(X_train, y_train)

    train_r2 = r2_score(y_train, lr.predict(X_train))
    test_r2 = r2_score(y_test, lr.predict(X_test))

    return lr, scaler, poly, X.columns, train_r2, test_r2

# ---------------------------
# Page configuration
# ---------------------------
st.set_page_config(page_title="🏡 King County House Sales", layout="wide")
st.title("🏡 King County House Sales Dashboard")
st.markdown(
    "This dashboard explores **house sales data** in King County (Seattle area) "
    "and also includes a **price forecasting model** based on property features."
)

# ---------------------------
# Load and train
# ---------------------------
df_filtered = load_data()
lr, scaler, poly, feature_cols, train_r2, test_r2 = train_model(df_filtered)

# ---------------------------
# Model performance
# ---------------------------
st.subheader("🤖 Price Forecasting Model")
c1, c2 = st.columns(2)
c1.metric("Train R²", f"{train_r2:.4f}")
c2.metric("Test R²",  f"{test_r2:.4f}")

# ---------------------------
# Prediction form
# ---------------------------
st.subheader("🔮 Predict House Price")

bedrooms        = st.number_input("Bedrooms", min_value=0, value=3)
bathrooms       = st.number_input("Bathrooms", min_value=0.0, value=2.0, step=0.5)
sqft_living     = st.number_input("Sqft Living", min_value=0, value=2000)
sqft_lot        = st.number_input("Sqft Lot", min_value=0, value=5000)
floors          = st.number_input("Floors", min_value=0.0, value=1.0, step=0.5)
waterfront      = st.selectbox("Waterfront", [0, 1])
view            = st.slider("View", 0, 4, 0)
condition       = st.slider("Condition", 1, 5, 3)
grade           = st.slider("Grade", 1, 13, 7)
sqft_above      = st.number_input("Sqft Above", min_value=0, value=1500)
sqft_basement   = st.number_input("Sqft Basement", min_value=0, value=500)
yr_renovated    = st.number_input("Year Renovated", min_value=0, max_value=2015, value=0)
lat             = st.number_input("Latitude", value=47.5)
long            = st.number_input("Longitude", value=-122.2)
sqft_living15   = st.number_input("Sqft Living 15", min_value=0, value=1800)
sqft_lot15      = st.number_input("Sqft Lot 15", min_value=0, value=4000)
year_built      = st.number_input("Year Built", min_value=1900, max_value=2015, value=2000)
age_of_house    = df_filtered['yr_built'].max() - year_built

zip_choices = sorted(df_filtered['zipcode'].unique().tolist())
zipcode_val = st.selectbox("Zipcode", zip_choices)

# Build input row
input_df = pd.DataFrame([{
    "bedrooms": bedrooms,
    "bathrooms": bathrooms,
    "sqft_living": sqft_living,
    "sqft_lot": sqft_lot,
    "floors": floors,
    "waterfront": waterfront,
    "view": view,
    "condition": condition,
    "grade": grade,
    "sqft_above": sqft_above,
    "sqft_basement": sqft_basement,
    "yr_renovated": yr_renovated,
    "lat": lat,
    "long": long,
    "sqft_living15": sqft_living15,
    "sqft_lot15": sqft_lot15,
    "age_of_house": age_of_house,
    "zipcode": zipcode_val
}])

# Match training features
if "zipcode" in input_df.columns:
    input_df = pd.get_dummies(input_df, columns=["zipcode"], drop_first=True)
input_df = input_df.reindex(columns=feature_cols, fill_value=0)

# Transform & predict
if st.button("Predict Price"):
    input_scaled = scaler.transform(input_df)
    input_poly = poly.transform(input_scaled)
    pred = lr.predict(input_poly)[0]
    st.success(f"💵 Estimated Price: ${pred:,.0f}")
