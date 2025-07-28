import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from io import BytesIO
from datetime import datetime

# PAGE CONFIG
st.set_page_config(page_title="SmartSell Premium Dashboard", page_icon="📊", layout="wide")

# MODE SOMBRE / CLAIR
mode = st.sidebar.radio("Mode", ["💡 Light", "🌙 Dark"])
if mode == "🌙 Dark":
    st.markdown("""<style>body{background-color:#1e1e1e;color:white;}</style>""", unsafe_allow_html=True)

# HEADER
st.markdown("""
# 📊 SmartSell Premium Dashboard
**Empowering Sales & Marketing with Data Intelligence**
""")
st.caption("🎯 Built by YourName — #OpenToWork #DataAnalytics")

# LOAD DATA (EXEMPLE SIMULÉ)
@st.cache_data
def load_data():
    np.random.seed(1)
    df = pd.DataFrame({
        "Product_Name": np.random.choice(["A", "B", "C", "D"], 200),
        "Category": np.random.choice(["Tech", "Beauty", "Sports"], 200),
        "Sub_Category": np.random.choice(["Sub1", "Sub2", "Sub3"], 200),
        "Price": np.random.randint(100, 2000, 200),
        "Rating": np.random.uniform(2, 5, 200),
        "Success_Percentage": np.random.uniform(10, 95, 200),
        "Sales_y": np.random.randint(500, 50000, 200),
        "M_Spend": np.random.randint(1000, 10000, 200),
    })
    return df

df = load_data()
filtered_df = df  # pas de filtre pour démo

# INSIGHT IA AUTOMATIQUE
avg_price = filtered_df["Price"].mean()
med_price = filtered_df["Price"].median()
if avg_price > med_price:
    insight = f"💡 Your average price ({avg_price:.0f}€) is **above** the market median ({med_price:.0f}€)."
else:
    insight = f"💡 Your average price ({avg_price:.0f}€) is **below** the market median ({med_price:.0f}€)."
st.success(insight)

# GRAPHE RADAR
st.markdown("### 📊 Category Success Radar")
radar_df = df.groupby("Category")[["Rating", "Success_Percentage", "Sales_y"]].mean().reset_index()
fig_radar = go.Figure()
for _, row in radar_df.iterrows():
    fig_radar.add_trace(go.Scatterpolar(
        r=[row["Rating"], row["Success_Percentage"], row["Sales_y"]/1000],
        theta=["Rating", "Success %", "Sales (K)"],
        fill='toself',
        name=row["Category"]
    ))
fig_radar.update_layout(polar=dict(radialaxis=dict(visible=True)), showlegend=True)
st.plotly_chart(fig_radar, use_container_width=True)

# EXPORT
def convert_df(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Data")
    return output.getvalue()

if st.button("📤 Export Report"):
    st.balloons()
    st.success("✅ Report ready!")
    st.download_button("⬇️ Download Excel", convert_df(filtered_df), "SmartSell_Report.xlsx")

# ZONE DE FEEDBACK
st.markdown("### 💬 Aidez-nous à améliorer ce produit")
feedback = st.text_area("Vos suggestions")
if feedback:
    st.success("Merci pour votre retour 💙")

# DONNÉES BRUTES
with st.expander("🔍 Show Raw Data"):
    st.dataframe(filtered_df, use_container_width=True)