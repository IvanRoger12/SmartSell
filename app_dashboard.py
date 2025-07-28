
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="SmartSell • Dashboard", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>📊 SmartSell Dashboard</h1>
    <p>Interactive Sales & Marketing KPIs</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

st.sidebar.title("🔎 Filters")
selected_categories = st.sidebar.multiselect("Select Categories", df["Category"].unique(), default=list(df["Category"].unique()))
price_range = st.sidebar.slider("Price Range (€)", int(df["Price"].min()), int(df["Price"].max()), (int(df["Price"].min()), int(df["Price"].max())))
rating_min = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.0, 0.1)

df_filtered = df[
    (df["Category"].isin(selected_categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= rating_min)
]

col1, col2, col3, col4 = st.columns(4)
col1.metric("💰 Revenue", f"{(df_filtered['Price'] * df_filtered['Sales_y']).sum():,.0f}€")
col2.metric("⭐ Avg Rating", f"{df_filtered['Rating'].mean():.1f}/5")
col3.metric("📈 Success Rate", f"{df_filtered['Success_Percentage'].mean():.1f}%")
col4.metric("📦 Products", len(df_filtered))

st.markdown("### 📊 Success by Category")
fig1 = px.bar(df_filtered.groupby("Category")[["Success_Percentage"]].mean().reset_index(), x="Category", y="Success_Percentage", color="Category")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 🎯 Price vs Success")
fig2 = px.scatter(df_filtered, x="Price", y="Success_Percentage", size="Sales_y", color="Category", hover_data=["Product_Name"])
st.plotly_chart(fig2, use_container_width=True)

st.markdown("### 📥 Raw Data")
st.dataframe(df_filtered, use_container_width=True)
