
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from io import BytesIO

# ==== CONFIGURATION ====
st.set_page_config(page_title="SmartSell Premium", page_icon="🚀", layout="wide")

# ==== CSS ====
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 12px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}
.metric-card {
    background-color: white;
    border-left: 6px solid #764ba2;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.05);
}
.stButton > button {
    background-color: #764ba2;
    color: white;
    border-radius: 5px;
}
</style>
""", unsafe_allow_html=True)

# ==== DONNÉES ====
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")
df = load_data()

# ==== HEADER ====
st.markdown("""
<div class="main-header">
    <h1>📊 SmartSell Premium Dashboard</h1>
    <p>Empowering Marketing & Sales Decisions with Intelligent Data Insights</p>
</div>
""", unsafe_allow_html=True)

# ==== SIDEBAR ====
st.sidebar.header("🎛️ Filters")
categories = st.sidebar.multiselect("Categories", df["Category"].unique(), default=list(df["Category"].unique()))
price_range = st.sidebar.slider("Price Range (€)", int(df["Price"].min()), int(df["Price"].max()), (int(df["Price"].min()), int(df["Price"].max())))
min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.0, 0.1)
search_term = st.sidebar.text_input("🔍 Search Product")

filtered_df = df[(df["Category"].isin(categories)) &
                 (df["Price"].between(price_range[0], price_range[1])) &
                 (df["Rating"] >= min_rating)]
if search_term:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_term, case=False)]

# ==== METRICS ====
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("💰 Total Revenue", f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")
    st.markdown('</div>', unsafe_allow_html=True)
with col2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("⭐ Avg Rating", f"{filtered_df['Rating'].mean():.2f}/5")
    st.markdown('</div>', unsafe_allow_html=True)
with col3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("🎯 Success Rate", f"{filtered_df['Success_Percentage'].mean():.1f}%")
    st.markdown('</div>', unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("📦 Product Count", f"{filtered_df.shape[0]}")
    st.markdown('</div>', unsafe_allow_html=True)

# ==== VISUALS ====
st.subheader("📊 Success Rate by Category")
fig1 = px.bar(filtered_df.groupby("Category", as_index=False)["Success_Percentage"].mean(),
              x="Category", y="Success_Percentage", color="Category", title="Success by Category")
st.plotly_chart(fig1, use_container_width=True)

st.subheader("🎯 Price vs Success Analysis")
fig2 = px.scatter(filtered_df, x="Price", y="Success_Percentage", size="Sales_Yearly", color="Rating",
                  hover_data=["Product_Name"], title="Bubble Chart: Price vs Success")
st.plotly_chart(fig2, use_container_width=True)

# ==== AI-RECOMMENDATION SECTION ====
st.markdown("## 💡 AI-Based Insights for Business Strategy")
col1, col2 = st.columns(2)
with col1:
    st.markdown("### 📉 Products Needing Attention")
    warning_df = filtered_df[filtered_df["Success_Percentage"] < 30]
    st.dataframe(warning_df[["Product_Name", "Success_Percentage", "M_Spend"]].sort_values(by="Success_Percentage"), use_container_width=True)
with col2:
    st.markdown("### 💰 Price Optimization Picks")
    boost_df = filtered_df[(filtered_df["Success_Percentage"] > 60) & (filtered_df["Price"] > filtered_df["Price"].median())]
    st.dataframe(boost_df[["Product_Name", "Price", "Success_Percentage", "Rating"]].sort_values(by="Price", ascending=False), use_container_width=True)

# ==== TIMELINE EFFECT ====
st.subheader("📈 Simulated Trend Over Time (Demo)")
df["Year"] = np.random.choice([2022, 2023, 2024], len(df))
trend_df = df.groupby("Year", as_index=False)["Success_Percentage"].mean()
fig_trend = px.line(trend_df, x="Year", y="Success_Percentage", markers=True, title="Average Success Over Time")
st.plotly_chart(fig_trend, use_container_width=True)

# ==== EXPORT BUTTON ====
st.markdown("## 📤 Export Report")
def convert_df_to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine="openpyxl")
    df.to_excel(writer, index=False, sheet_name="SmartSell_Report")
    writer.close()
    return output.getvalue()

excel_data = convert_df_to_excel(filtered_df)
st.download_button("📥 Download Excel Report", data=excel_data, file_name="SmartSell_Report.xlsx", mime="application/vnd.ms-excel")

# ==== FOOTER ====
st.markdown("---")
st.markdown("<p style='text-align: center;'>👤 Created with ❤️ by IvanRoger12 • Connect on LinkedIn • Powered by Streamlit & Plotly</p>", unsafe_allow_html=True)
