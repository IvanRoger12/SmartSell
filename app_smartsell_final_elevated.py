
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# --------------- Page config --------------------
st.set_page_config(page_title="SmartSell Premium Dashboard", page_icon="🚀", layout="wide")

# --------------- Light/Dark Theme Toggle --------------------
theme_mode = st.sidebar.radio("🌗 Display Mode", ["Light", "Dark"], horizontal=True)

if theme_mode == "Dark":
    st.markdown(
        """
        <style>
            body {
                background-color: #121212;
                color: #FFFFFF;
            }
            .stApp {
                background-color: #121212;
                color: #FFFFFF;
            }
        </style>
        """, unsafe_allow_html=True)
else:
    st.markdown(
        """
        <style>
            body {
                background-color: #FFFFFF;
                color: #000000;
            }
            .stApp {
                background-color: #FFFFFF;
                color: #000000;
            }
        </style>
        """, unsafe_allow_html=True)

# --------------- Données simulées --------------------
@st.cache_data
def load_data():
    np.random.seed(42)
    return pd.DataFrame({
        'Product_Name': ['Product A', 'Product B', 'Product C', 'Product D'] * 25,
        'Category': ['Home', 'Sports', 'Beauty', 'Tech'] * 25,
        'Sub_Category': ['Kitchen', 'Camping', 'Makeup', 'Gadget'] * 25,
        'Price': np.random.randint(100, 1500, 100),
        'Rating': np.random.uniform(3.0, 5.0, 100),
        'Success_Percentage': np.random.uniform(30, 90, 100),
        'Sales_Yearly': np.random.randint(1000, 100000, 100),
        'M_Spend': np.random.uniform(500, 10000, 100)
    })

with st.spinner("🔄 Loading insights..."):
    df = load_data()

# --------------- Mode d'affichage --------------------
view_mode = st.radio("🔍 Choose display mode", ["Minimalist", "Detailed"], horizontal=True)

if view_mode == "Detailed":
    st.markdown("### 📊 Detailed Performance View")
    st.dataframe(df, use_container_width=True)
else:
    st.markdown("### 🧼 Minimalist View Enabled")

# --------------- Graphique Sunburst pour sous-catégories --------------------
st.markdown("### 🌞 Category & Sub-category Explorer")
fig_sun = px.sunburst(
    df,
    path=['Category', 'Sub_Category'],
    values='Sales_Yearly',
    color='Success_Percentage',
    color_continuous_scale='RdBu',
    title="Sunburst View by Category/Sub-Category"
)
st.plotly_chart(fig_sun, use_container_width=True)

# --------------- Graphique Funnel --------------------
st.markdown("### 📈 Conversion Funnel")
funnel_df = pd.DataFrame({
    "Stage": ["Visited", "Interested", "Added to Cart", "Purchased"],
    "Users": [10000, 7000, 3000, 1200]
})
fig_funnel = px.funnel(funnel_df, x='Users', y='Stage', title="Sales Funnel Simulation")
st.plotly_chart(fig_funnel, use_container_width=True)

# --------------- Insight IA --------------------
st.markdown("### 🤖 AI Insight")
median_price = df['Price'].median()
avg_price = df['Price'].mean()
msg = "✅ Your average price is competitive!" if avg_price <= median_price else "⚠️ Your average price is above the market median."
st.success(msg)

# --------------- Footer UX --------------------
st.markdown("---")
st.markdown("### 💬 Help Us Improve")
feedback = st.text_area("Leave a suggestion or comment about this dashboard")
if st.button("📨 Submit Feedback"):
    st.success("Thanks for your feedback! 💡")

st.caption("🎯 Built by [Ton nom], #OpenToWork — Powered by Streamlit")

