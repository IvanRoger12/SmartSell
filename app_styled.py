# SmartSell – Elegant Visual Version

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page config
st.set_page_config(page_title="SmartSell", layout="wide", page_icon="📊")

# CSS
st.markdown("""
<style>
body {
    background-color: #f8f9fa;
}
h1 {
    color: #4a4a4a;
}
.metric-box {
    background: linear-gradient(135deg, #89f7fe 0%, #66a6ff 100%);
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}
.hero {
    background: linear-gradient(to right, #667eea, #764ba2);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    margin-bottom: 2rem;
    text-align: center;
}
.block {
    background-color: white;
    padding: 2rem;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 2rem;
}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

def calculate_kpis(df):
    if df.empty:
        return {'revenue': 0, 'roi': 0, 'success': 0, 'count': 0}
    revenue = (df['Price'] * df['Sales_y']).sum()
    spend = df['M_Spend'].sum()
    roi = ((revenue - spend) / spend) * 100 if spend > 0 else 0
    success = df['Success_Percentage'].mean()
    return {
        'revenue': revenue,
        'roi': roi,
        'success': success,
        'count': len(df)
    }

def show_dashboard(df):
    st.markdown('<div class="hero"><h1>📊 SmartSell Dashboard</h1><p>Business Intelligence for Sales & Marketing</p></div>', unsafe_allow_html=True)

    st.sidebar.header("🎛️ Filters")
    categories = st.sidebar.multiselect("Category", df['Category'].unique(), default=list(df['Category'].unique()))
    threshold = st.sidebar.slider("Success Threshold (%)", 0, 100, 0)
    filtered = df[(df['Category'].isin(categories)) & (df['Success_Percentage'] >= threshold)]

    if filtered.empty:
        st.warning("⚠️ No data matches the filters.")
        return

    kpis = calculate_kpis(filtered)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"<div class='metric-box'><h3>Total Revenue</h3><h2>${kpis['revenue']:,.0f}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'><h3>ROI</h3><h2>{kpis['roi']:.1f}%</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'><h3>Success Rate</h3><h2>{kpis['success']:.1f}%</h2></div>", unsafe_allow_html=True)
    with col4:
        st.markdown(f"<div class='metric-box'><h3>Products</h3><h2>{kpis['count']}</h2></div>", unsafe_allow_html=True)

    st.markdown("### 📂 Category Overview")
    cat_df = filtered.groupby('Category').agg({
        'Success_Percentage': 'mean',
        'Sales_y': 'sum',
        'M_Spend': 'sum'
    }).reset_index()
    fig = make_subplots(rows=1, cols=3, subplot_titles=["Success %", "Sales", "Marketing Spend"])
    fig.add_trace(go.Bar(x=cat_df['Category'], y=cat_df['Success_Percentage'], name='Success'), 1, 1)
    fig.add_trace(go.Bar(x=cat_df['Category'], y=cat_df['Sales_y'], name='Sales'), 1, 2)
    fig.add_trace(go.Bar(x=cat_df['Category'], y=cat_df['M_Spend'], name='Spend'), 1, 3)
    fig.update_layout(height=500, showlegend=False)
    st.plotly_chart(fig, use_container_width=True)

def show_recommendations(df):
    st.markdown('<div class="hero"><h1>💡 Smart Recommendations</h1><p>AI-Powered Business Insights</p></div>', unsafe_allow_html=True)

    df = df.copy()
    high_cost_low_result = df[(df['M_Spend'] > df['M_Spend'].median()) & (df['Success_Percentage'] < df['Success_Percentage'].median())]
    overpriced = df[(df['Price'] > df['Price'].quantile(0.75)) & (df['Success_Percentage'] < 50)]

    if not high_cost_low_result.empty:
        st.markdown("#### 📢 Inefficient Marketing Spend")
        st.dataframe(high_cost_low_result[['Product_Name', 'Category', 'M_Spend', 'Success_Percentage']].head(10))

    if not overpriced.empty:
        st.markdown("#### 💰 Price Optimization Opportunities")
        st.dataframe(overpriced[['Product_Name', 'Category', 'Price', 'Success_Percentage']].head(10))

def main():
    df = load_data()
    page = st.sidebar.selectbox("Navigate", ["📊 Dashboard", "💡 Recommendations"])
    if page == "📊 Dashboard":
        show_dashboard(df)
    else:
        show_recommendations(df)

if __name__ == "__main__":
    main()
