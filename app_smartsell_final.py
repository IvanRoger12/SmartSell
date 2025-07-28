
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(
    page_title="SmartSell Dashboard",
    page_icon="📊",
    layout="wide"
)

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# -------- SIDEBAR --------
st.sidebar.header("🧰 Filters")
selected_categories = st.sidebar.multiselect(
    "Select Categories",
    options=df["Category"].unique(),
    default=df["Category"].unique()
)

price_range = st.sidebar.slider(
    "Price Range (€)",
    min_value=int(df["Price"].min()),
    max_value=int(df["Price"].max()),
    value=(int(df["Price"].min()), int(df["Price"].max()))
)

rating_min = st.sidebar.slider(
    "Minimum Rating",
    min_value=1.0,
    max_value=5.0,
    value=3.0,
    step=0.1
)

search_product = st.sidebar.text_input("🔍 Search by Product", "")

# -------- FILTERING --------
filtered_df = df[
    (df["Category"].isin(selected_categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= rating_min)
]

if search_product:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_product, case=False)]

# -------- HEADER --------
st.markdown("""
<div style="background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            padding: 2rem; border-radius: 10px; color: white; text-align: center;">
    <h1>📊 SmartSell Dashboard</h1>
    <p>Premium Business Insights for Sales & Marketing</p>
</div>
""", unsafe_allow_html=True)

# -------- KPIs --------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("💰 Total Revenue", f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")
with col2:
    st.metric("⭐ Avg Rating", f"{filtered_df['Rating'].mean():.1f}/5")
with col3:
    st.metric("✅ Success Rate", f"{filtered_df['Success_Percentage'].mean():.1f}%")
with col4:
    st.metric("📦 Products", len(filtered_df))

# -------- VISUALS --------
st.markdown("### 📈 Success by Category")
fig_cat = px.bar(
    filtered_df.groupby("Category").agg({"Success_Percentage": "mean"}).reset_index(),
    x="Category", y="Success_Percentage",
    color="Category",
    color_discrete_sequence=px.colors.qualitative.Pastel
)
st.plotly_chart(fig_cat, use_container_width=True)

st.markdown("### 🎯 Price vs Success")
fig_scatter = px.scatter(
    filtered_df,
    x="Price", y="Success_Percentage",
    color="Category",
    size="Sales_y",
    hover_data=["Product_Name", "Rating"],
    color_discrete_sequence=px.colors.qualitative.Bold
)
st.plotly_chart(fig_scatter, use_container_width=True)

# -------- STRATEGIC INSIGHTS --------
st.markdown("## 🧠 Strategic Insights & Recommendations")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📉 Inefficient Marketing Spend")
    inefficient = filtered_df[filtered_df["Success_Percentage"] < 50].sort_values("M_Spend", ascending=False)
    st.dataframe(inefficient[["Product_Name", "Category", "M_Spend", "Success_Percentage"]].head(10), use_container_width=True)

with col2:
    st.markdown("### 💡 Price Optimization Opportunities")
    price_opt = filtered_df[filtered_df["Rating"] > 4].sort_values("Price")
    st.dataframe(price_opt[["Product_Name", "Price", "Rating", "Success_Percentage"]].head(10), use_container_width=True)

# -------- FOOTER --------
st.markdown("---")
st.markdown("<center>Made with 💜 by IvanRoger12 | Powered by Streamlit & ChatGPT</center>", unsafe_allow_html=True)
