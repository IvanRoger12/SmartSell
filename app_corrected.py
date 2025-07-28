# SmartSell – Corrected Version for Streamlit Cloud

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="SmartSell - Business Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

def calculate_kpis(df):
    total_revenue = (df['Price'] * df['Sales_y']).sum()
    total_marketing_spend = df['M_Spend'].sum()
    roi = ((total_revenue - total_marketing_spend) / total_marketing_spend) * 100
    avg_success_rate = df['Success_Percentage'].mean()
    top_performer = df.loc[df['Success_Percentage'].idxmax(), 'Product_Name']

    return {
        'total_revenue': total_revenue,
        'total_marketing_spend': total_marketing_spend,
        'roi': roi,
        'avg_success_rate': avg_success_rate,
        'top_performer': top_performer,
        'total_products': len(df)
    }

def create_category_chart(df):
    category_stats = df.groupby('Category').agg({
        'Success_Percentage': 'mean',
        'Sales_y': 'sum',
        'M_Spend': 'sum'
    }).reset_index()

    fig = make_subplots(rows=1, cols=3, subplot_titles=["Success %", "Sales", "Marketing Spend"])

    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['Success_Percentage'], name='Success %'), row=1, col=1)
    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['Sales_y'], name='Sales'), row=1, col=2)
    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['M_Spend'], name='Marketing Spend'), row=1, col=3)

    fig.update_layout(height=500, title="📊 Category Performance Overview", showlegend=False)
    return fig

def main():
    st.title("📊 SmartSell – Business Intelligence Dashboard")

    df = load_data()
    if df is None:
        return

    st.sidebar.header("Filters")
    selected_categories = st.sidebar.multiselect("Select Categories", df['Category'].unique(), default=list(df['Category'].unique()))
    success_threshold = st.sidebar.slider("Min Success %", 0, 100, 0)

    filtered_df = df[(df['Category'].isin(selected_categories)) & (df['Success_Percentage'] >= success_threshold)]

    st.subheader("📈 Key Metrics")
    kpis = calculate_kpis(filtered_df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", f"${kpis['total_revenue']:,.0f}")
    col2.metric("ROI", f"{kpis['roi']:.2f}%")
    col3.metric("Success Rate", f"{kpis['avg_success_rate']:.1f}%")
    col4.metric("Products", f"{kpis['total_products']}")

    st.subheader("📊 Category Overview")
    fig = create_category_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
