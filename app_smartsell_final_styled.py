import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import io
from datetime import datetime

st.set_page_config(

    page_title="SmartSell Premium Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 🌍 Language selector
language = st.sidebar.selectbox("🌍 Language / Langue", ["English", "Français"])
def t(english, french):
    return french if language == "Français" else english

# --- Load dataset ---
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")
df = load_data()

# --- Sidebar filters ---
st.sidebar.header(t("Filters", "Filtres"))
categories = st.sidebar.multiselect(
    t("Select Categories", "Sélectionner les catégories"),
    options=df["Category"].unique(),
    default=list(df["Category"].unique())
)
price_range = st.sidebar.slider(
    t("Price Range (€)", "Gamme de prix (€)"),
    int(df["Price"].min()), int(df["Price"].max()),
    (int(df["Price"].min()), int(df["Price"].max()))
)
min_rating = st.sidebar.slider(
    t("Minimum Rating", "Note minimale"),
    1.0, 5.0, 3.0, step=0.1
)
search_term = st.sidebar.text_input(t("Search by Product", "Rechercher un produit"), "")

filtered_df = df[
    (df["Category"].isin(categories)) &
    (df["Price"].between(price_range[0], price_range[1])) &
    (df["Rating"] >= min_rating)
]
if search_term:
    filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_term, case=False)]

# --- Tabs ---
tab1, tab2 = st.tabs([t("📊 Dashboard", "📊 Tableau de bord"), t("💡 Insights & Actions", "💡 Insights & Actions")])

with tab1:
    st.title(t("SmartSell Premium Dashboard", "Tableau de bord SmartSell Premium"))
    st.markdown(t("Empowering Marketing & Sales Decisions with Intelligent Data Insights", "Des décisions marketing & commerciales basées sur la donnée"))

    c1, c2, c3, c4 = st.columns(4)
    c1.metric(t("💰 Total Revenue", "💰 Chiffre d'affaires"), f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")
    c2.metric(t("⭐ Avg Rating", "⭐ Note moyenne"), f"{filtered_df['Rating'].mean():.2f}/5")
    c3.metric(t("🎯 Success Rate", "🎯 Taux de succès"), f"{filtered_df['Success_Percentage'].mean():.1f}%")
    c4.metric(t("📦 Product Count", "📦 Nombre de produits"), f"{len(filtered_df)}")

    st.subheader(t("Success Rate by Category", "Taux de succès par catégorie"))
    cat_stats = filtered_df.groupby("Category", as_index=False)["Success_Percentage"].mean()
    fig1 = px.bar(cat_stats, x="Category", y="Success_Percentage", color="Category")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader(t("Price vs Success Analysis", "Analyse Prix vs Succès"))
    fig2 = px.scatter(
        filtered_df, x="Price", y="Success_Percentage",
        size="Sales_y", color="Rating", hover_data=["Product_Name"]
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader(t("Trend Over Time", "Tendance au fil du temps"))
    df["Year"] = np.random.choice([2022, 2023, 2024], len(df))
    trend = df.groupby("Year", as_index=False)["Success_Percentage"].mean()
    fig3 = px.line(trend, x="Year", y="Success_Percentage", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.title(t("Insights & Actions", "Insights & Actions"))
    st.subheader(t("🚀 High Potential Products", "🚀 Produits à fort potentiel"))
    high_pot = filtered_df[(filtered_df["Rating"] >= 4.0) & (filtered_df["Success_Percentage"] < filtered_df["Success_Percentage"].median())]
    st.dataframe(high_pot[["Product_Name", "Rating", "Price", "Success_Percentage"]].head(10), use_container_width=True)

    st.subheader(t("💰 Price Optimization Picks", "💰 Opportunités de prix"))
    overpriced = filtered_df[(filtered_df["Price"] > filtered_df["Price"].quantile(0.75)) & (filtered_df["Success_Percentage"] < 50)]
    st.dataframe(overpriced[["Product_Name", "Price", "Success_Percentage"]].head(10), use_container_width=True)

    st.subheader(t("Export Report", "Export du rapport"))
    def to_excel(df_):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df_.to_excel(writer, index=False, sheet_name="Report")
        output.seek(0)
        return output
    st.download_button(
        label=t("Download Excel Report", "Télécharger Excel"),
        data=to_excel(filtered_df),
        file_name=f"SmartSell_Report_{datetime.now().strftime('%Y%m%d')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    with st.expander(t("Show raw data", "Afficher les données brutes")):
        st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.markdown(f"<center>© {datetime.now().year} IvanRoger12 | Streamlit & Plotly</center>", unsafe_allow_html=True)



# 🎨 CUSTOM DESIGN STYLE
st.markdown("""
<style>
body {
    background: linear-gradient(to bottom, #f4f4f4, #ffffff);
}
.big-title {
    font-size: 40px;
    color: #4c6ef5;
    font-weight: bold;
    text-align: center;
    margin-top: -30px;
}
.metric-card {
    background-color: #ffffff;
    border-left: 5px solid #4c6ef5;
    padding: 15px;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
</style>
<div class="big-title">🚀 SmartSell Premium Dashboard</div>
""", unsafe_allow_html=True)
