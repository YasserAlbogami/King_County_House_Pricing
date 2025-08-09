# 🏡 King County House Sales Dashboard

Welcome to the King County House Sales Dashboard!  
This project provides an interactive **Streamlit** application to explore house sales data from King County (Seattle area) and forecast prices using a **Ridge Regression model**.

---

## 🧭 Project Overview

The dashboard allows users to:

- Explore housing features and their impact on sale prices.
- View interactive visualizations for property characteristics.
- Predict house prices by entering custom property details.

**Tech Stack:**  
- Python, Streamlit, Pandas, Plotly, Scikit-learn  
- Directory structure:  
  - `pages/` (dashboard pages)
  - `tabs/` (visualization and analysis tabs)
  - `data/` (dataset)
  - `requirements.txt` (dependencies list)

---

## 🚀 How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/YasserAlbogami/King_County_House_Pricing.git
cd King_County_House_Pricing
````

### 2. Set Up a Virtual Environment

Recommended for clean dependency management:

```bash
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
streamlit run Home.py
```

---

## 🏗️ Dashboard Pages & Tabs

### Entry Page: `Home.py`

* **Purpose:** Landing page and project introduction.
* **Features:**

  * Overview of the dataset.
  * Link to dashboard pages.

---

### Dashboard Pages

#### 1. **General Insights** (`tabs/general_insights.py`)

* Distribution and comparison of price by:

  * Lot size category
  * Square footage
  * View quality
  * House condition
  * Renovation status

#### 2. **Numerical Analysis** (`tabs/numrecial_analysis.py`)

* Average house age
* Average price by waterfront status
* Correlation heatmaps between selected features
* Average price by number of floors and bedrooms
* Monthly sales trends

#### 3. **Price Forecasting Model**

* Based on **Ridge Regression** with polynomial features.
* Includes:

  * Feature scaling
  * One-hot encoding of zipcode
  * Prediction form for custom inputs

---

## 📂 Directory Structure

```
King_County_House_Pricing/
├── Home.py                     # Main landing page
├── pages/                      # Additional Streamlit pages
│   └── Linear_Model.py         # Price forecasting model UI
├── tabs/
│   ├── general_insights.py     # General insights plots
│   ├── numrecial_analysis.py   # Numerical analysis plots
├── data/
│   └── kc_house_data.csv       # Dataset
├── requirements.txt
└── README.md
```

---

## 🙋 Contributing

Pull requests and suggestions are welcome! If you’d like to enhance the model, improve the UI, or add new analyses, feel free to open an issue or PR.

## 📜 License

MIT License

```

Do you want me to also include **sample screenshots** like in some GitHub READMEs so the project looks more appealing? That could make it pop for viewers.
```
