import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Config de la page
st.set_page_config(
    page_title="SmartSell – Premium Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Chargement des données
@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

# Supprimer la colonne Unnamed si présente
if "Unnamed: 0" in df.columns:
    df = df.drop(columns=["Unnamed: 0"])

# Header stylé
st.markdown("""
    <div style="background: linear-gradient(90deg, #667eea, #764ba2); padding: 1.5rem 1rem; border-radius: 8px; color: white; text-align: center;">
        <h1 style="margin: 0;">📊 SmartSell Dashboard</h1>
        <p style="margin: 0;">Premium Business Insights for Sales & Marketing</p>
    </div>
    """, unsafe_allow_html=True)

# Sidebar filtres
st.sidebar.header("🎛️ Filters")

categories = st.sidebar.multiselect("Select Categories", df["Category"].unique(), default=list(df["Category"].unique()))
price_min, price_max = st.sidebar.slider("Price Range (€)", int(df["Price"].min()), int(df["Price"].max()), (int(df["Price"].min()), int(df["Price"].max())))
rating_threshold = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.0, 0.1)

search_query = st.sidebar.text_input("🔍 Search by Product Name")

# Filtrage
filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Price"].between(price_min, price_max)) &
    (df["Rating"] >= rating_threshold)
]

if search_query:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_query, case=False)]

# KPIs
st.markdown("### 📈 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Revenue", f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")
col2.metric("⭐ Avg Rating", f"{filtered_df['Rating'].mean():.2f}/5")
col3.metric("🎯 Success Rate", f"{filtered_df['Success_Percentage'].mean():.1f}%" if not filtered_df.empty else "0%")
col4.metric("📦 Products", f"{filtered_df.shape[0]}")

# Graphiques principaux
st.markdown("### 📊 Success by Category")
category_perf = filtered_df.groupby("Category").agg({
    "Success_Percentage": "mean",
    "Sales_y": "sum"
}).reset_index()

fig1 = px.bar(category_perf, x="Category", y="Success_Percentage", color="Sales_y", color_continuous_scale="viridis", title="Average Success Rate by Category")
st.plotly_chart(fig1, use_container_width=True)

st.markdown("### 🎯 Price vs Success")
fig2 = px.scatter(
    filtered_df, x="Price", y="Success_Percentage",
    size="Sales_y", color="Rating", hover_data=["Product_Name"],
    color_continuous_scale="plasma"
)
st.plotly_chart(fig2, use_container_width=True)

# -------------------- PAGE 2 : INSIGHTS --------------------
st.markdown("---")
st.markdown("## 🧠 Strategic Insights & Recommendations")

# Inefficient spend
st.markdown("### 💸 Inefficient Marketing Spend")
low_performance = filtered_df[filtered_df["Success_Percentage"] < 50].sort_values("Success_Percentage").head(10)
st.dataframe(low_performance[["Product_Name", "Category", "M_Spend", "Success_Percentage"]], use_container_width=True)

# Opportunities
st.markdown("### 📌 Price Optimization Opportunities")
high_price_low_success = filtered_df[
    (filtered_df["Price"] > filtered_df["Price"].mean()) &
    (filtered_df["Success_Percentage"] < filtered_df["Success_Percentage"].mean())
]
top_opp = high_price_low_success.sort_values("Price", ascending=False).head(10)
st.dataframe(top_opp[["Product_Name", "Price", "Success_Percentage", "Rating"]], use_container_width=True)

# Corrélation
st.markdown("### 🔍 Correlation Heatmap")
corr_df = filtered_df[["Price", "Rating", "Success_Percentage", "Sales_y", "M_Spend"]].corr()
fig3 = px.imshow(corr_df, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
st.plotly_chart(fig3, use_container_width=True)

# Export bouton
st.markdown("---")
colA, colB = st.columns(2)
with colA:
    if st.button("🔄 Refresh"):
        st.cache_data.clear()
        st.rerun()
with colB:
    st.markdown("📆 Last Update: Now")

# Fin
st.markdown("---")
st.markdown("💡 *SmartSell is built for data-driven sales & marketing teams looking to optimize performance and gain strategic insights.*")