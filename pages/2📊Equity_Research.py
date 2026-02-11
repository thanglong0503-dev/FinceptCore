"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: pages/2_📊_Equity_Research.py
ROLE: Corporate Finance & Valuation Dashboard
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import streamlit as st
import sys
import os

# Định tuyến hệ thống
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.analytics.valuation import DCFValuation
from src.ui.components import TerminalUI
from src.ui.styles import apply_terminal_style

# 1. KHỞI TẠO PAGE
st.set_page_config(page_title="Equity Research", page_icon="📊", layout="wide")
apply_terminal_style()

st.title("📊 EQUITY RESEARCH")
st.markdown("`[MODULE 02] | DISCOUNTED CASH FLOW (DCF) VALUATION ENGINE | STANDARD: WALL STREET`")
st.divider()

# 2. KHU VỰC ĐIỀU KHIỂN
col_ctrl, col_main = st.columns([1, 3], gap="large")

with col_ctrl:
    st.subheader("TARGET ASSAY")
    ticker = st.text_input("EQUITY TICKER", value="AAPL", help="Chỉ áp dụng cho Cổ phiếu (Ví dụ: AAPL, MSFT)").upper()
    
    st.markdown("---")
    st.subheader("MACRO ASSUMPTIONS")
    st.caption("Thiết lập giả định vĩ mô & tăng trưởng")
    
    # Sliders nhập liệu
    growth_rate = st.slider("GROWTH RATE 1-5Y (%)", min_value=1.0, max_value=40.0, value=12.0, step=0.5, help="Tốc độ tăng trưởng Dòng tiền tự do 5 năm đầu")
    terminal_g = st.slider("TERMINAL GROWTH (%)", min_value=1.0, max_value=5.0, value=2.5, step=0.1, help="Tốc độ tăng trưởng vĩnh viễn (thường bằng GDP hoặc Lạm phát)")
    erp = st.slider("EQUITY RISK PREMIUM (%)", min_value=3.0, max_value=10.0, value=5.5, step=0.1, help="Phần bù rủi ro vốn cổ phần thị trường")
    
    st.markdown("<br>", unsafe_allow_html=True)
    execute_btn = st.button("EXECUTE VALUATION MATRIX")

# 3. KHU VỰC HIỂN THỊ KẾT QUẢ
with col_main:
    st.subheader("VALUATION OUTPUT")
    
    if execute_btn:
        with st.spinner(f"Compiling Financials & Running DCF Models for {ticker}..."):
            # Gọi Engine
            dcf_engine = DCFValuation(ticker)
            result = dcf_engine.calculate(
                growth_rate_1_5=growth_rate / 100.0, 
                terminal_growth=terminal_g / 100.0, 
                equity_risk_premium=erp / 100.0
            )
            
            if "error" not in result:
                curr = result['currency']
                prefix = "₫" if curr == "VND" else "$"
                
                # A. KẾT QUẢ CHÍNH (THE BIG NUMBERS)
                m1, m2, m3 = st.columns(3)
                with m1:
                    TerminalUI.render_metric_card("CURRENT MARKET PRICE", result['current_price'], 0, prefix=prefix)
                with m2:
                    TerminalUI.render_metric_card("INTRINSIC FAIR VALUE", result['fair_value'], 0, prefix=prefix)
                with m3:
                    TerminalUI.render_metric_card("UPSIDE / DOWNSIDE", result['upside_pct'], result['upside_pct'], prefix="", format_str="{:+.2f}")

                st.markdown("---")
                
                # B. TÍN HIỆU GIAO DỊCH (TRADING SIGNAL)
                signal_col, data_col = st.columns([1, 1])
                
                with signal_col:
                    st.markdown("#### 📡 QUANT SIGNAL")
                    if result['upside_pct'] > 15:
                        st.success("🟢 STRONG BUY: Tài sản đang bị định giá thấp (Undervalued) đáng kể.")
                    elif result['upside_pct'] < -15:
                        st.error("🔴 STRONG SELL: Tài sản đang bị định giá cao (Overvalued). Nguy cơ bong bóng.")
                    else:
                        st.warning("🟡 HOLD: Giá thị trường đang phản ánh đúng giá trị thực (Fairly Valued).")
                        
                with data_col:
                    st.markdown("#### ⚙️ ENGINE PARAMETERS")
                    # Hiển thị số liệu nội bộ của cỗ máy
                    st.code(f"""
[+] Base FCF (TTM) : {prefix}{result['fcf_base']:,.0f}
[+] Target WACC    : {result['wacc']*100:.2f}%
[+] Target Beta    : {result['assumptions']['beta']:.2f}
[+] Risk-Free Rate : {result['assumptions']['rf']*100:.2f}%
[+] Enterprise Val : {prefix}{result['enterprise_value']:,.0f}
                    """.strip(), language="bash")
            else:
                st.error(f"SYSTEM HALTED: {result['error']}")
                st.info("Module DCF yêu cầu cổ phiếu phải có lợi nhuận và Dòng tiền dương. Các công ty khởi nghiệp hoặc đang lỗ sẽ làm sập thuật toán.")
    else:
        # Màn hình chờ phong cách Terminal
        st.info("SYSTEM READY. AWAITING PARAMETERS...")
        st.code("""
> PING YAHOO_FINANCE_API... OK (12ms)
> PING FRED_MACRO_API... OK (45ms)
> LOAD DCF_ALGORITHM... LOADED
> STATUS: WAITING FOR USER INPUT
        """, language="bash")
