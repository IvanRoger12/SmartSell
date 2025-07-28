
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="SmartSell • Insights", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&display=swap');
    html, body, [class*="css"] {
        font-family: 'Poppins', sans-serif;
    }
    .main-header {
        background: linear-gradient(90deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    .insight-box {
        background: white;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        border-left: 5px solid #4facfe;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="main-header">
    <h1>💡 SmartSell Insights</h1>
    <p>AI-powered suggestions and product intelligence</p>
</div>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

df = load_data()

st.sidebar.title("🔎 Filters")
selected_categories = st.sidebar.multiselect("Select Categories", df["Category"].unique(), default=list(df["Category"].unique()))

df_filtered = df[df["Category"].isin(selected_categories)]

st.markdown("### 📌 Smart Recommendations")

# Insight: high potential but underperforming
potential = df_filtered[
    (df_filtered["Rating"] >= 4.0) &
    (df_filtered["Success_Percentage"] < df_filtered["Success_Percentage"].median())
]

if not potential.empty:
    st.markdown(f"<div class='insight-box'><strong>🚀 {len(potential)} high-potential products</strong> have strong ratings but low success. Consider boosting their visibility.</div>", unsafe_allow_html=True)

# Insight: overpriced products
overpriced = df_filtered[
    (df_filtered["Price"] > df_filtered["Price"].quantile(0.75)) &
    (df_filtered["Success_Percentage"] < 50)
]

if not overpriced.empty:
    st.markdown(f"<div class='insight-box'><strong>💸 {len(overpriced)} overpriced products</strong> are underperforming. Consider a pricing review.</div>", unsafe_allow_html=True)

# Insight: inefficient marketing
inefficient = df_filtered[
    (df_filtered["M_Spend"] > df_filtered["M_Spend"].median()) &
    (df_filtered["Success_Percentage"] < df_filtered["Success_Percentage"].median())
]

if not inefficient.empty:
    st.markdown(f"<div class='insight-box'><strong>📉 {len(inefficient)} products</strong> have high marketing spend but low success. Optimize marketing efforts.</div>", unsafe_allow_html=True)

st.markdown("### 📊 Correlation Analysis")
corr_matrix = df_filtered[["Price", "Rating", "Success_Percentage", "Sales_y", "M_Spend"]].corr()
fig_corr = px.imshow(corr_matrix, text_auto=True, aspect="auto", color_continuous_scale="RdBu_r")
st.plotly_chart(fig_corr, use_container_width=True)

st.markdown("### 📥 Export Recommendations")
st.download_button("⬇️ Download Filtered Data (CSV)", df_filtered.to_csv(index=False).encode("utf-8"), "smart_insights.csv", "text/csv")

st.markdown("### 🔎 Raw Data")
st.dataframe(df_filtered, use_container_width=True)
