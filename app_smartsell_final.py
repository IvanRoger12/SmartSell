import streamlit as st

# 🌍 Language selector
language = st.sidebar.selectbox("🌍 Language / Langue", ["English", "Français"])

# Translations
def t(english, french):
    return french if language == "Français" else english

import pandas as pd
import plotly.express as px
import numpy as np
import io
from datetime import datetime

st.set_page_config(
    page_title="SmartSell Premium Dashboard",
    layout="wide",
    page_icon="📈"
)

@st.cache_data
def load_data():
    df = pd.read_csv("dataset.csv")
    return df

def main():
    df = load_data()

    # ---- FILTERS ----
    st.sidebar.title("🔍 Filters")
    category_filter = st.sidebar.multiselect("Select Categories", df['Category'].unique(), default=list(df['Category'].unique()))
    price_range = st.sidebar.slider("Price Range (€)", int(df['Price'].min()), int(df['Price'].max()), (int(df['Price'].min()), int(df['Price'].max())))
    min_rating = st.sidebar.slider("Minimum Rating", 1.0, 5.0, 3.0, step=0.1)

    df_filtered = df[
        (df['Category'].isin(category_filter)) &
        (df['Price'].between(price_range[0], price_range[1])) &
        (df['Rating'] >= min_rating)
    ]

    tab1, tab2 = st.tabs(["📊 Dashboard", "💡 Insights & Actions"])

    with tab1:
        st.title(t("📊 SmartSell Premium Dashboard", "📊 Tableau de bord SmartSell Premium"))
        st.markdown("Empowering Marketing & Sales Decisions with Intelligent Data Insights")

        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric(t("💰 Total Revenue", "💰 Chiffre d'affaires"), f"{(df_filtered['Price'] * df_filtered['Sales_y']).sum():,.0f}€")
        with col2:
            st.metric(t("⭐ Avg Rating", "⭐ Note moyenne"), f"{df_filtered['Rating'].mean():.2f}/5")
        with col3:
            st.metric(t("🎯 Success Rate", "🎯 Taux de succès"), f"{df_filtered['Success_Percentage'].mean():.1f}%")
        with col4:
            st.metric(t("📦 Product Count", "📦 Nombre de produits"), len(df_filtered))

        # Bar chart
        st.subheader("📊 Success Rate by Category")
        category_stats = df_filtered.groupby("Category")["Success_Percentage"].mean().reset_index()
        fig1 = px.bar(category_stats, x="Category", y="Success_Percentage", color="Success_Percentage", color_continuous_scale="bluered")
        st.plotly_chart(fig1, use_container_width=True)

        # Bubble chart
        st.subheader("🎯 Price vs Success Analysis")
        fig2 = px.scatter(df_filtered, x="Price", y="Success_Percentage", size="Sales_y", color="Rating",
                          hover_data=["Product_Name"], title="Bubble Chart: Price vs Success")
        st.plotly_chart(fig2, use_container_width=True)

        # Search bar
        st.subheader("🔎 Search Products")
        search_term = st.text_input("Enter product name or part of it...")
        if search_term:
            st.dataframe(df_filtered[df_filtered["Product_Name"].str.contains(search_term, case=False)], use_container_width=True)

    with tab2:
        st.title("💡 AI-Based Insights for Business Strategy")

        # High potential products
        high_potential = df_filtered[
            (df_filtered['Rating'] >= 4.0) &
            (df_filtered['Success_Percentage'] < df_filtered['Success_Percentage'].median())
        ]
        st.markdown("### 🚀 High Potential Products")
        st.dataframe(high_potential[['Product_Name', 'Rating', 'Price', 'Success_Percentage']].head(10), use_container_width=True)

        # Price optimization
        overpriced = df_filtered[
            (df_filtered['Price'] > df_filtered['Price'].quantile(0.75)) &
            (df_filtered['Success_Percentage'] < 50)
        ]
        st.markdown("### 💰 Price Optimization Picks")
        st.dataframe(overpriced[['Product_Name', 'Price', 'Success_Percentage']].head(10), use_container_width=True)

        # Export CSV
        st.markdown("### 📤 Export Report")
        def convert_df_to_excel(df):
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name="SmartSell Report")
            output.seek(0)
            return output

        excel_data = convert_df_to_excel(df_filtered)
        st.download_button("Download Excel Report", data=excel_data, file_name=f"SmartSell_Report_{datetime.now().strftime('%Y%m%d')}.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

        # Raw data (optional)
        with st.expander("🔍 Show raw data"):
            st.dataframe(df_filtered, use_container_width=True)

if __name__ == "__main__":
    main()