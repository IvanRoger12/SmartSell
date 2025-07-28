
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO
import base64

# ------------------ Config Page ------------------
st.set_page_config(
    page_title="🚀 SmartSell Premium Dashboard",
    page_icon="📈",
    layout="wide",
)

# ------------------ CSS Animation ------------------
st.markdown("""
<style>
@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
  100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
}
.header {
    animation: pulse 2s infinite;
    background: linear-gradient(90deg, #667eea, #764ba2);
    padding: 2rem;
    border-radius: 12px;
    text-align: center;
    color: white;
    font-size: 30px;
    font-weight: bold;
    margin-bottom: 2rem;
}
</style>
<div class="header">🚀 SmartSell Premium Dashboard</div>
""", unsafe_allow_html=True)

# ------------------ Dataset Load ------------------
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

df = load_data()

# ------------------ Language Switch ------------------
lang = st.sidebar.selectbox("🌍 Language / Langue", ["English", "Français"])

def t(en, fr):
    return en if lang == "English" else fr

# ------------------ Sidebar Filters ------------------
st.sidebar.header(t("Filters", "Filtres"))

categories = st.sidebar.multiselect(
    t("Select Categories", "Sélectionner les catégories"),
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

search_input = st.sidebar.text_input(t("🔍 Search by Product", "🔍 Rechercher un produit"))

# ------------------ Data Filtering ------------------
filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= rating_min)
]

if search_input:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_input, case=False)]

# ------------------ Metrics ------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(t("💰 Total Revenue", "💰 Chiffre d'affaires"),
              f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")

with col2:
    st.metric("⭐ " + t("Avg Rating", "Note moyenne"),
              f"{filtered_df['Rating'].mean():.2f}/5")

with col3:
    st.metric(t("🎯 Success Rate", "🎯 Taux de succès"),
              f"{filtered_df['Success_Percentage'].mean():.1f}%")

with col4:
    st.metric("📦 " + t("Product Count", "Nombre de produits"),
              len(filtered_df))

# ------------------ Visuals ------------------
st.markdown(f"### 📊 {t('Success Rate by Category', 'Taux de succès par catégorie')}")
fig1 = px.bar(
    filtered_df.groupby("Category")["Success_Percentage"].mean().reset_index(),
    x="Category", y="Success_Percentage", color="Category",
    title=t("Average Success Rate by Category", "Taux de succès moyen par catégorie"),
    color_discrete_sequence=px.colors.qualitative.Set2
)
st.plotly_chart(fig1, use_container_width=True)

st.markdown(f"### 🎯 {t('Price vs Success Analysis', 'Analyse Prix vs Succès')}")
fig2 = px.scatter(
    filtered_df,
    x="Price", y="Success_Percentage",
    size="Sales_y", color="Rating",
    hover_data=["Product_Name"],
    title=t("Bubble Chart: Price vs Success", "Nuage de points : Prix vs Succès"),
    color_continuous_scale="viridis"
)
st.plotly_chart(fig2, use_container_width=True)

# ------------------ Trend Graph ------------------
st.markdown(f"### 📈 {t('Trend Over Time', 'Tendance au fil du temps')}")
filtered_df["Year"] = pd.to_datetime("2025", format="%Y")
trend_data = filtered_df.groupby(filtered_df["Year"].dt.year)["Success_Percentage"].mean().reset_index()
fig_trend = px.line(trend_data, x="Year", y="Success_Percentage", markers=True)
st.plotly_chart(fig_trend, use_container_width=True)

# ------------------ Export Option ------------------
def convert_df_to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="SmartSell")
    return output.getvalue()

excel = convert_df_to_excel(filtered_df)

st.download_button(
    label="📤 " + t("Download Report", "Télécharger le rapport"),
    data=excel,
    file_name="SmartSell_Report.xlsx",
    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)
