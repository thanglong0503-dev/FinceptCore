import streamlit as st
import pandas as pd
from src.backend.market import MarketEngine
from src.analytics.valuation import ValuationEngine
from src.ui.styles import apply_terminal_style

apply_terminal_style()
st.title("📊 INSTITUTIONAL EQUITY RESEARCH")

col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("### 1. TARGET SELECTION")
    ticker = st.text_input("Analyze Ticker", "AAPL").upper()
    fund_data = MarketEngine.get_fundamentals(ticker)
    
    if fund_data and 'info' in fund_data:
        info = fund_data['info']
        st.image(info.get('logo_url', ''), width=50)
        st.write(f"**Sector:** {info.get('sector', 'N/A')}")
        st.write(f"**Beta:** {info.get('beta', 'N/A')}")
        st.write(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
        
        st.markdown("### 2. DCF ASSUMPTIONS")
        growth = st.slider("Growth Rate (5y)", 0.0, 0.4, 0.12)
        wacc = st.slider("WACC (Discount)", 0.05, 0.20, 0.09)
        term_g = st.number_input("Terminal Growth", 0.02)
        
        # Auto-extract inputs if possible
        try:
            fcf = fund_data['cashflow'].loc['Free Cash Flow'].iloc
            debt = fund_data['balance_sheet'].loc.iloc if 'Total Debt' in fund_data['balance_sheet'].index else 0
            cash = fund_data['balance_sheet'].loc['Cash And Cash Equivalents'].iloc
            shares = info.get('sharesOutstanding', 1)
        except:
            st.warning("Auto-extraction failed. Using manual inputs.")
            fcf = st.number_input("FCF (Latest)", 1_000_000_000)
            debt = st.number_input("Total Debt", 0)
            cash = st.number_input("Cash", 0)
            shares = st.number_input("Shares Outstanding", 100_000_000)

with col2:
    st.markdown("### 3. VALUATION MODEL OUTPUT")
    
    if st.button("RUN DCF SIMULATION", type="primary"):
        res = ValuationEngine.calculate_dcf(
            fcf=fcf,
            growth_rate=growth,
            terminal_growth=term_g,
            discount_rate=wacc,
            net_debt=(debt - cash),
            shares=shares
        )
        
        current_price = info.get('currentPrice', 1.0)
        upside = ((res['fair_value'] - current_price) / current_price) * 100
        
        m1, m2, m3 = st.columns(3)
        m1.metric("INTRINSIC VALUE", f"${res['fair_value']:.2f}")
        m2.metric("CURRENT PRICE", f"${current_price}")
        m3.metric("UPSIDE/DOWNSIDE", f"{upside:.2f}%", delta_color="normal")
        
        st.success("MODEL EXECUTION COMPLETE")
        st.json(res)
    else:
        st.info("System Ready. Awaiting Execution Command.")
        
    # Financial Statement Viewer
    st.markdown("---")
    st.markdown("### 4. FINANCIAL STATEMENTS")
    tab1, tab2 = st.tabs()
    if fund_data:
        with tab1: st.dataframe(fund_data['financials'], height=400)
        with tab2: st.dataframe(fund_data['balance_sheet'], height=400)
