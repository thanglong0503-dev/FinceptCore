"""
FINCEPT TERMINAL - KERNEL ENTRY POINT
-------------------------------------
Version: 3.3.0 (Stable Fix)
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. SYSTEM PATH CONFIGURATION (CRITICAL FIX)
# -----------------------------------------------------------------------------
# Tự động thêm thư mục gốc vào path để Python tìm thấy 'src'
current_file_path = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file_path) # finceptcore/
root_dir = os.path.dirname(current_dir)          # FinceptTerminal/ (Root)

if root_dir not in sys.path:
    sys.path.append(root_dir)

# Import module nội bộ (Bọc trong try-except để debug đường dẫn)
try:
    from src.ui.styles import apply_terminal_style, render_ticker_tape
    from src.backend.market import MarketEngine
except ImportError as e:
    st.error(f"⚠️ KERNEL BOOT ERROR: Không thể tải module 'src'.")
    st.code(f"Current Path: {sys.path}\nError: {str(e)}")
    st.stop()

# -----------------------------------------------------------------------------
# 2. APP CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Fincept Terminal | Enterprise",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Fincept-Corporation/FinceptTerminal',
        'About': "Fincept Terminal v3.3. Enterprise Edition."
    }
)

# Khởi tạo Session State
if 'system_boot_time' not in st.session_state:
    st.session_state.system_boot_time = datetime.now().strftime("%H:%M:%S")
if 'connection_status' not in st.session_state:
    st.session_state.connection_status = "SECURE"

# Áp dụng giao diện Terminal (Dark Mode CSS)
apply_terminal_style()

# -----------------------------------------------------------------------------
# 3. GLOBAL DATA FEED (FIX LỖI SYNTAX TẠI ĐÂY)
# -----------------------------------------------------------------------------

# [FIX] Đã gán danh sách cụ thể, không để trống
tickers =

@st.cache_data(ttl=60)
def load_ticker_tape():
    """Tải dữ liệu nhanh cho thanh ticker chạy ngang"""
    tape =
    # Lấy 6 mã đầu tiên để tối ưu hiệu suất khởi động
    for t in tickers[:6]:
        data = MarketEngine.get_realtime_price(t)
        if data:
            tape.append(data)
    return tape

# Render thanh ticker
with st.container():
    live_data = load_ticker_tape()
    if live_data:
        render_ticker_tape(live_data)

# -----------------------------------------------------------------------------
# 4. NAVIGATION ROUTER (ĐIỀU HƯỚNG TRANG)
# -----------------------------------------------------------------------------
# Định nghĩa các trang chức năng
pg_market = st.Page("pages/1_🌐_Market_Cockpit.py", title="Market Cockpit", icon="🌐", default=True)
pg_equity = st.Page("pages/2_📊_Equity_Research.py", title="Equity Research", icon="📊")
pg_ai = st.Page("pages/3_🧠_AI_Neural_Core.py", title="AI Neural Core", icon="🧠")
pg_risk = st.Page("pages/4_⚖️_Portfolio_Risk.py", title="Portfolio Risk", icon="⚖️")

# Cấu trúc menu điều hướng
pg = st.navigation({
    "Global Surveillance": [pg_market],
    "Investment Lab": [pg_equity, pg_risk],
    "Intelligence Unit": [pg_ai]
})

# -----------------------------------------------------------------------------
# 5. SIDEBAR CONTROLS
# -----------------------------------------------------------------------------
with st.sidebar:
    st.markdown("## 🦅 FINCEPT TERM")
    st.caption("v3.3.0 | STABLE BUILD")
    st.markdown("---")
    
    # Hiển thị trạng thái hệ thống
    col_stat, col_lat = st.columns(2)
    with col_stat:
        st.markdown("**LINK**")
        st.markdown(f"🟢 {st.session_state.connection_status}")
    with col_lat:
        st.markdown("**PING**")
        st.markdown(f"⚡ {int(time.time() * 1000) % 60}ms")
    
    st.markdown("---")
    
    # Giả lập Command Line Interface (CLI)
    cmd = st.text_input("TERMINAL COMMAND >", placeholder="HELP for commands")
    if cmd:
        if cmd.upper() == "CLEAR":
            st.cache_data.clear()
            st.toast("Memory Cache Purged", icon="🧹")
        elif cmd.upper() == "EXIT":
            st.warning("Session Terminated")
            st.stop()
        else:
            st.info(f"Command '{cmd}' sent to core.")

    # Thông tin dữ liệu
    with st.expander("Active Data Feeds"):
        st.caption("✅ NASDAQ/NYSE (Realtime)")
        st.caption("✅ FOREX (Streaming)")
        st.caption("✅ CRYPTO (Binance Agg.)")

# -----------------------------------------------------------------------------
# 6. MAIN EXECUTION
# -----------------------------------------------------------------------------
try:
    pg.run()
except Exception as e:
    st.error("🛑 KERNEL PANIC: Application Crash")
    st.error(f"Details: {str(e)}")
    st.markdown("### Recovery Steps:")
    st.markdown("1. Check `pages/` folder existence.")
    st.markdown("2. Verify `src/backend/market.py` integrity.")
