import streamlit as st
import numpy as np
import pandas as pd
import plotly.express as px
from src.ui.styles import apply_terminal_style

apply_terminal_style()
st.title("⚖️ RISK MANAGEMENT & VaR")

st.sidebar.header("Portfolio Construction")
tickers = st.sidebar.text_input("Assets (comma separated)", "AAPL, MSFT, GOOG, GLD, BTC-USD")
weights_str = st.sidebar.text_input("Weights (comma separated)", "0.2, 0.2, 0.2, 0.2, 0.2")

if st.button("CALCULATE RISK METRICS"):
    # Mock Data Generation
    asset_list = [x.strip() for x in tickers.split(",")]
    weight_list = [float(x) for x in weights_str.split(",")]
    
    # Create fake returns for demo
    dates = pd.date_range(start="2023-01-01", periods=252)
    data = pd.DataFrame(index=dates)
    for asset in asset_list:
        data[asset] = np.random.normal(0, 0.015, 252) # Fake daily returns
        
    # Portfolio Returns
    data['Portfolio'] = data.dot(weight_list)
    
    # Calculate VaR
    conf_level = 0.95
    var_95 = np.percentile(data['Portfolio'], (1 - conf_level) * 100)
    cvar_95 = data['Portfolio'][data['Portfolio'] <= var_95].mean()
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Daily VaR (95%)", f"{var_95*100:.2f}%")
    c2.metric("CVaR / Expected Shortfall", f"{cvar_95*100:.2f}%")
    c3.metric("Sharpe Ratio (Ann.)", f"{(data['Portfolio'].mean()/data['Portfolio'].std()) * np.sqrt(252):.2f}")
    
    st.subheader("Distribution of Returns")
    fig = px.histogram(data, x="Portfolio", nbins=50, title="Portfolio Returns Distribution", color_discrete_sequence=['#00FF41'])
    fig.add_vline(x=var_95, line_dash="dash", line_color="red", annotation_text="VaR 95%")
    fig.update_layout(template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
