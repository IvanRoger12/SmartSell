
import streamlit as st
import pandas as pd
from utils.data_loader import load_data
from utils.analytics import calculate_kpis
from utils.insights import generate_insights
from visuals.plots import plot_sales_by_category

# Page config
st.set_page_config(page_title="SmartSell", layout="wide")

# Logo & Title
st.title("📊 SmartSell – Intelligent Sales & Marketing Dashboard")

# Load data
df = load_data()

# Business Context
st.markdown("### 💼 Business Objective")
st.markdown("""
SmartSell is designed to help **Sales & Marketing teams** gain full visibility over product performance and marketing impact.
By combining product data, sales trends, and marketing efforts, SmartSell delivers actionable insights to improve ROI and operational efficiency.
""")

# KPIs
st.markdown("### 🔢 Key Performance Indicators")
kpis = calculate_kpis(df)
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales (Y)", f"{kpis['total_sales']:,}")
col2.metric("Average Price", f"${kpis['average_price']:.2f}")
col3.metric("Average Rating", f"{kpis['average_rating']:.1f} ⭐")

# Visualization
st.markdown("### 📈 Sales by Category")
fig = plot_sales_by_category(df)
st.plotly_chart(fig, use_container_width=True)

# Insights
st.markdown("### 💡 Smart Insights")
st.dataframe(generate_insights(df), use_container_width=True)
