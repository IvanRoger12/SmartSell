
import streamlit as st
import pandas as pd
import plotly.express as px
from io import BytesIO

# -------------------- Configuration --------------------
st.set_page_config(
    page_title="🚀 SmartSell Premium Dashboard",
    page_icon="📈",
    layout="wide"
)

# -------------------- Style CSS --------------------
st.markdown("""
<style>
    .main-header {
        font-size: 2.5em;
        color: white;
        background: linear-gradient(90deg, #667eea, #764ba2);
        padding: 1rem 2rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 1.5rem;
        font-weight: bold;
        box-shadow: 2px 2px 12px rgba(0,0,0,0.2);
    }
    .insight-box {
        background-color: #f8f9fa;
        border-left: 5px solid #667eea;
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

# -------------------- Données --------------------
@st.cache_data
def load_data():
    return pd.read_csv("dataset.csv")

df = load_data()

# -------------------- Interface Langue --------------------
lang = st.sidebar.selectbox("🌍 Language / Langue", ["English", "Français"])
def t(en, fr): return en if lang == "English" else fr

# -------------------- Tabs --------------------
tab1, tab2 = st.tabs(["📊 Dashboard", "💡 AP Insights"])

with tab1:
    st.markdown("<div class='main-header'>📊 SmartSell Premium Dashboard</div>", unsafe_allow_html=True)

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
        min_value=1.0, max_value=5.0, value=3.0, step=0.1
    )

    search_input = st.sidebar.text_input(t("🔍 Search by Product", "🔍 Rechercher un produit"))

    filtered_df = df[
        (df["Category"].isin(categories)) &
        (df["Price"].between(price_range[0], price_range[1])) &
        (df["Rating"] >= rating_min)
    ]
    if search_input:
        filtered_df = filtered_df[filtered_df["Product_Name"].str.contains(search_input, case=False)]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("💰 " + t("Total Revenue", "Chiffre d'affaires"),
                  f"{(filtered_df['Price'] * filtered_df['Sales_y']).sum():,.0f}€")
    with col2:
        st.metric("⭐ " + t("Avg Rating", "Note moyenne"),
                  f"{filtered_df['Rating'].mean():.2f}/5")
    with col3:
        st.metric("🎯 " + t("Success Rate", "Taux de succès"),
                  f"{filtered_df['Success_Percentage'].mean():.1f}%")
    with col4:
        st.metric("📦 " + t("Product Count", "Nombre de produits"), len(filtered_df))

    st.markdown("### 📊 " + t("Success Rate by Category", "Taux de succès par catégorie"))
    fig1 = px.bar(
        filtered_df.groupby("Category")["Success_Percentage"].mean().reset_index(),
        x="Category", y="Success_Percentage", color="Category"
    )
    st.plotly_chart(fig1, use_container_width=True)

    st.markdown("### 🎯 " + t("Price vs Success Analysis", "Analyse Prix vs Succès"))
    fig2 = px.scatter(
        filtered_df,
        x="Price", y="Success_Percentage",
        size="Sales_y", color="Rating",
        hover_data=["Product_Name"],
        color_continuous_scale="viridis"
    )
    st.plotly_chart(fig2, use_container_width=True)

    st.markdown("### 📈 " + t("Trend Over Time", "Tendance au fil du temps"))
    filtered_df["Year"] = 2025
    trend_data = filtered_df.groupby("Year")["Success_Percentage"].mean().reset_index()
    fig3 = px.line(trend_data, x="Year", y="Success_Percentage", markers=True)
    st.plotly_chart(fig3, use_container_width=True)

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

with tab2:
    st.markdown("<div class='main-header'>💡 Insights & Actions</div>", unsafe_allow_html=True)

    st.markdown("""
    <div class="insight-box">
        ✅ <strong>Marketing Optimization:</strong> Some categories are overspending with low ROI. Consider reallocating budget to higher-performing segments.
    </div>
    <div class="insight-box">
        🛒 <strong>Weak Products:</strong> A few products show low success rates and ratings. Evaluate pricing strategy or consider product improvement/removal.
    </div>
    <div class="insight-box">
        📈 <strong>Hidden Opportunities:</strong> Products with high ratings but low marketing spend could perform better with targeted investment.
    </div>
    <div class="insight-box">
        🔍 <strong>Category Focus:</strong> Focus more on high-performing categories such as Beauty & Health or Sports where ROI is significantly better.
    </div>
    """, unsafe_allow_html=True)

