
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Set page config
st.set_page_config(page_title="SmartSell Premium", layout="wide")

# Custom Google Font + Styling
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;600;800&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Poppins', sans-serif;
        background: #f9f9fb;
    }

    .main-header {
        font-size: 3em;
        font-weight: 800;
        color: #ffffff;
        background: linear-gradient(to right, #667eea, #764ba2);
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
    }

    .kpi-box {
        background: linear-gradient(to right, #4facfe, #00f2fe);
        padding: 1.2rem;
        border-radius: 15px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        color: white;
        text-align: center;
    }

    .section-title {
        font-size: 1.5em;
        font-weight: 600;
        margin: 1rem 0;
        color: #333;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="main-header">📊 SmartSell Premium — Sales & Marketing Intelligence</div>', unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.title("🔍 Filters")
selected_category = st.sidebar.multiselect("Category", df["Category"].unique(), default=df["Category"].unique())

df_filtered = df[df["Category"].isin(selected_category)]

# KPIs
total_revenue = (df_filtered["Price"] * df_filtered["Sales_Yearly"]).sum()
roi = ((total_revenue - df_filtered["Marketing_Spend"].sum()) / df_filtered["Marketing_Spend"].sum()) * 100
avg_success = df_filtered["Success_Percentage"].mean()
total_products = len(df_filtered)

col1, col2, col3, col4 = st.columns(4)
col1.markdown(f'<div class="kpi-box"><h4>Total Revenue</h4><h2>${total_revenue:,.0f}</h2></div>', unsafe_allow_html=True)
col2.markdown(f'<div class="kpi-box"><h4>ROI</h4><h2>{roi:.1f}%</h2></div>', unsafe_allow_html=True)
col3.markdown(f'<div class="kpi-box"><h4>Success Rate</h4><h2>{avg_success:.1f}%</h2></div>', unsafe_allow_html=True)
col4.markdown(f'<div class="kpi-box"><h4>Products</h4><h2>{total_products}</h2></div>', unsafe_allow_html=True)

# Visualisation
st.markdown('<div class="section-title">📈 Sales Overview by Category</div>', unsafe_allow_html=True)
fig = px.bar(df_filtered.groupby("Category").sum(numeric_only=True).reset_index(),
             x="Category", y="Sales_Yearly", color="Category",
             title="Yearly Sales by Category", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# Export Button
csv = df_filtered.to_csv(index=False).encode('utf-8')
st.download_button("⬇️ Export Filtered Data (CSV)", csv, "smart_filtered_data.csv", "text/csv")

# Business Insight
st.markdown('<div class="section-title">💡 Business Insight</div>', unsafe_allow_html=True)
if avg_success > 60:
    st.success("Your current product portfolio is performing well. Keep investing in your best categories.")
elif avg_success > 40:
    st.warning("Moderate success rate. Identify weak areas and consider marketing or pricing strategies.")
else:
    st.error("Your success rate is low. Strategic revision required on multiple fronts.")

# Signature
st.markdown("---")
st.markdown("✨ Built with ❤️ by IvanRoger12 | #SmartSell #BusinessIntelligence #Streamlit")
