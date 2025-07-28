# SmartSell Standalone Streamlit App

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Page configuration
st.set_page_config(
    page_title="SmartSell - Business Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for styling
st.markdown("""
<style>
.metric-container {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1.5rem;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin: 1rem 0;
}
.insight-box {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    padding: 1.5rem;
    border-radius: 15px;
    color: white;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("dataset.csv")
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

# Calculate KPIs
def calculate_kpis(df):
    total_revenue = (df['Price'] * df['Sales_Yearly']).sum()
    total_marketing_spend = df['Marketing_Spend'].sum()
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

# Create category chart
def create_category_performance_chart(df):
    category_stats = df.groupby('Category').agg({
        'Success_Percentage': 'mean',
        'Sales_Yearly': 'sum',
        'Marketing_Spend': 'sum'
    }).reset_index()

    fig = make_subplots(
        rows=1, cols=3,
        subplot_titles=('Success %', 'Sales', 'Marketing Spend'),
        specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
    )

    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['Success_Percentage'], name='Success'), row=1, col=1)
    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['Sales_Yearly'], name='Sales'), row=1, col=2)
    fig.add_trace(go.Bar(x=category_stats['Category'], y=category_stats['Marketing_Spend'], name='Marketing'), row=1, col=3)

    fig.update_layout(height=500, showlegend=False, title_text="Category Performance Overview")
    return fig

# Main Streamlit App
def main():
    st.title("📊 SmartSell – Business Intelligence Dashboard")

    df = load_data()
    if df is None:
        return

    # Sidebar filters
    st.sidebar.header("Filters")
    selected_categories = st.sidebar.multiselect("Select Categories", options=df['Category'].unique(), default=list(df['Category'].unique()))
    success_threshold = st.sidebar.slider("Min Success %", 0, 100, 0)

    filtered_df = df[(df['Category'].isin(selected_categories)) & (df['Success_Percentage'] >= success_threshold)]

    # KPIs
    st.subheader("📈 Key Metrics")
    kpis = calculate_kpis(filtered_df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Revenue", f"${kpis['total_revenue']:,.0f}")
    col2.metric("ROI", f"{kpis['roi']:.2f}%")
    col3.metric("Success Rate", f"{kpis['avg_success_rate']:.1f}%")
    col4.metric("Products", f"{kpis['total_products']}")

    # Charts
    st.subheader("📊 Category Overview")
    fig = create_category_performance_chart(filtered_df)
    st.plotly_chart(fig, use_container_width=True)

if __name__ == "__main__":
    main()
