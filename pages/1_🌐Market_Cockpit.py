"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: pages/1_🌐_Market_Cockpit.py
ROLE: Real-time Market Data Dashboard
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import streamlit as st
import sys
import os

# Nạp hệ thống thư viện Core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.backend.market import MarketDataEngine
from src.analytics.technical import TechnicalIndicators
from src.ui.components import TerminalUI
from src.ui.styles import apply_terminal_style

# 1. KHỞI TẠO PAGE
st.set_page_config(page_title="Market Cockpit", page_icon="🌐", layout="wide")
apply_terminal_style()

# 2. HEADER
st.title("🌐 MARKET COCKPIT")
st.markdown("`[MODULE 01] | REAL-TIME EQUITIES & CRYPTO SCANNER | ENGINE: YFINANCE`")
st.divider()

# 3. ĐIỀU KHIỂN BẢNG TÁP-LÔ (CONTROL PANEL)
col_ctrl, col_main = st.columns([1, 4], gap="large")

with col_ctrl:
    st.subheader("TARGET")
    ticker = st.text_input("TICKER SYMBOL", value="AAPL", help="Cổ phiếu (AAPL, VNM.HM) hoặc Crypto (BTC-USD)").upper()
    
    st.markdown("---")
    st.subheader("PARAMETERS")
    period = st.selectbox("TIME HORIZON", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "max"], index=3)
    interval = st.selectbox("RESOLUTION", ["1d", "1wk", "1mo"])
    
    st.markdown("---")
    st.caption("Auto-sync: Active")
    st.caption("Cache latency: <50ms")

# 4. KHU VỰC HIỂN THỊ CHÍNH (MAIN DISPLAY)
with col_main:
    with st.spinner(f"Establishing connection to global feeds for {ticker}..."):
        # Kéo dữ liệu từ Backend
        info = MarketDataEngine.get_company_info(ticker)
        df_raw = MarketDataEngine.get_historical_data(ticker, period, interval)
        
        if info and not "error" in info and df_raw is not None:
            # === PHẦN A: METRICS (Chỉ số nhanh) ===
            st.subheader(f"ENTITY: {info.get('name', ticker).upper()} | {info.get('exchange', 'N/A')}")
            
            m1, m2, m3, m4 = st.columns(4)
            curr_price = info.get('current_price', 0)
            prev_price = info.get('previous_close', 0)
            chg_abs, chg_pct = MarketDataEngine.calculate_price_change(curr_price, prev_price)
            
            with m1:
                TerminalUI.render_metric_card("LAST PRICE", curr_price, chg_pct, prefix=info.get('currency', '$') + " ")
            with m2:
                TerminalUI.render_metric_card("MARKET CAP", info.get('market_cap', 0) / 1e9, 0, prefix="$", format_str="{:,.2f}B")
            with m3:
                vol_ratio = (info.get('volume', 0) / info.get('avg_volume_10d', 1) * 100) if info.get('avg_volume_10d', 0) else 0
                TerminalUI.render_metric_card("VOLUME (vs 10d Avg)", info.get('volume', 0) / 1e6, vol_ratio - 100, prefix="", format_str="{:,.2f}M")
            with m4:
                TerminalUI.render_metric_card("P/E RATIO", info.get('pe_ratio', 0), 0, prefix="", format_str="{:.2f}x")
            
            st.markdown("---")
            
            # === PHẦN B: TÍNH TOÁN & VẼ BIỂU ĐỒ ===
            # Bơm các chỉ báo kỹ thuật vào Dataframe
            df_tech = TechnicalIndicators.add_all_indicators(df_raw)
            
            # Gọi hàm vẽ biểu đồ từ thư viện UI
            TerminalUI.render_advanced_chart(
                df_tech, 
                title=f"{ticker} - ACTION ZONE & VOLUME PROFILE", 
                show_volume=True
            )
            
            # === PHẦN C: DỮ LIỆU THÔ (DATA MATRIX) ===
            with st.expander("👁️ DEEP DIVE: RAW TECHNICAL MATRIX"):
                st.caption("Bảng dữ liệu OHLCV và các chỉ báo kỹ thuật (RSI, MACD, BB) của 30 phiên gần nhất.")
                # Lọc dữ liệu, đổi thứ tự ngày mới nhất lên trên cùng
                display_df = df_tech.tail(30).sort_index(ascending=False)
                TerminalUI.render_data_table(display_df, height=300)
                
        else:
            # Xử lý ngoại lệ đẹp mắt
            st.error(f"SYSTEM FAILURE: Unable to locate asset '{ticker}'.")
            st.info("💡 Hướng dẫn: Đảm bảo mã Ticker đúng định dạng của Yahoo Finance. Ví dụ: AAPL, TSLA, BTC-USD, VNM.HM")
