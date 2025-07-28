
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# ---------- Configuration générale ----------
st.set_page_config(page_title="SmartSell Premium", layout="wide", page_icon="📊")

st.markdown("""
    <style>
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
        .stSelectbox > div > div {
            background-color: #f8f9fa;
        }
        .sidebar .sidebar-content {
            background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
        }
    </style>
""", unsafe_allow_html=True)

# ---------- Chargement des données ----------
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# ---------- Sidebar : Navigation ----------
page = st.sidebar.radio("📂 Pages", ["📊 Dashboard", "💡 Insights"])

# ---------- Sidebar : Filtres généraux ----------
st.sidebar.markdown("## 🔍 Filters")
categories = st.sidebar.multiselect("Select Categories", options=df["Category"].unique(), default=list(df["Category"].unique()))
price_range = st.sidebar.slider("Price Range (€)", float(df["Price"].min()), float(df["Price"].max()), (float(df["Price"].min()), float(df["Price"].max())))
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.0, step=0.1)
product_search = st.sidebar.text_input("🔎 Search by Product", "")

# ---------- Filtrage ----------
filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= min_rating)
]

if product_search:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(product_search, case=False)]

# ---------- Page 1 : Dashboard ----------
if page == "📊 Dashboard":
    st.markdown("""
        <div class="main-header">
            <h1>📊 SmartSell Dashboard</h1>
            <p>Premium Business Insights for Sales & Marketing</p>
        </div>
    """, unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 Revenue", f"{(filtered_df['Price'] * filtered_df['Sales_Yearly']).sum():,.0f}€")
    with col2:
        st.metric("⭐ Avg Rating", f"{filtered_df['Rating'].mean():.1f}/5")
    with col3:
        st.metric("📈 Success Rate", f"{filtered_df['Success_Percentage'].mean():.0f}%")
    with col4:
        st.metric("📦 Products", f"{len(filtered_df)}")

    st.markdown("### 📊 Success by Category")
    cat_fig = px.bar(filtered_df.groupby("Category").agg({"Success_Percentage": "mean"}).reset_index(), x="Category", y="Success_Percentage", color="Category", title="Average Success Rate by Category")
    st.plotly_chart(cat_fig, use_container_width=True)

    st.markdown("### 🎯 Price vs Success")
    scatter_fig = px.scatter(filtered_df, x="Price", y="Success_Percentage", color="Rating", size="Sales_Yearly", hover_data=["Product_Name"], title="Price vs Success Rate")
    st.plotly_chart(scatter_fig, use_container_width=True)

# ---------- Page 2 : Insights ----------
if page == "💡 Insights":
    st.markdown("""
        <div class="main-header">
            <h1>💡 SmartSell Strategic Insights</h1>
            <p>AI-Powered Opportunities for Marketing & Sales</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("### 🚨 Inefficient Marketing Spend")
    inefficient = filtered_df[filtered_df["Success_Percentage"] < 30].sort_values(by="M_Spend", ascending=False).head(10)
    st.dataframe(inefficient[["Product_Name", "Category", "M_Spend", "Success_Percentage"]], use_container_width=True)

    st.markdown("### 💸 Price Optimization")
    price_opt = filtered_df[filtered_df["Success_Percentage"] > 60].sort_values(by="Price", ascending=False).head(10)
    st.dataframe(price_opt[["Product_Name", "Price", "Success_Percentage", "Rating"]], use_container_width=True)

    st.markdown("### 🔗 Correlation Matrix")
    corr_df = filtered_df[["Price", "Success_Percentage", "Rating", "Sales_Yearly", "M_Spend"]].corr()
    fig_corr = px.imshow(corr_df, text_auto=True, color_continuous_scale="Viridis")
    st.plotly_chart(fig_corr, use_container_width=True)
