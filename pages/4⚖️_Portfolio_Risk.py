# ==========================================
# FILE: pages/4_⚖️_Portfolio_Risk.py
# ==========================================
import streamlit as st
from src.analytics.risk import CFA_Math, CashFlow
from src.ui.styles import apply_terminal_style
import pandas as pd

st.set_page_config(page_title="Portfolio Risk", layout="wide")
apply_terminal_style()

st.title("⚖️ PORTFOLIO RISK & QUANT LAB")
st.markdown("`CFA STANDARD RISK METRICS & CAPITAL BUDGETING`")
st.divider()

t1, t2 = st.tabs(["Risk Metrics", "Project IRR"])

with t1:
    ret_str = st.text_area("Input Monthly Returns (%)", "2.5, -1.2, 3.8, 4.5, -2.0, 5.1")
    if st.button("COMPUTE RISK"):
        rets = [float(x.strip())/100 for x in ret_str.split(',')]
        prices = [100]
        for r in rets: prices.append(prices[-1] * (1+r))
        
        c1, c2 = st.columns(2)
        c1.metric("Sharpe Ratio", f"{CFA_Math.sharpe_ratio(rets):.2f}")
        c2.metric("Max Drawdown", f"{CFA_Math.max_drawdown(prices)*100:.2f}%", delta_color="inverse")
        st.line_chart(prices)

with t2:
    cf_data = st.data_editor(pd.DataFrame({'Year': [0, 1, 2, 3], 'CF': [-1000, 400, 400, 400]}))
    rate = st.slider("Discount Rate (%)", 1, 20, 10)/100
    if st.button("COMPUTE IRR/NPV"):
        cfs = [CashFlow(f"2026-01-0{int(r['Year'])+1}", r['CF']) for _, r in cf_data.iterrows()]
        st.metric("NPV", f"${CFA_Math.npv(cfs, rate):,.2f}")
        irr_val = CFA_Math.irr(cfs)
        st.metric("IRR", f"{irr_val*100:.2f}%" if irr_val else "Error")
