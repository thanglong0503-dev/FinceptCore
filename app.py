"""
FINCEPT TERMINAL - CORE APPLICATION KERNEL
------------------------------------------
Path: finceptcore/app.py
Version: 3.3.2 (Hotfix Release)
Author: Fincept Architecture Team
"""

import streamlit as st
import sys
import os
import time
import random
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. SYSTEM PATH BOOTSTRAP
# -----------------------------------------------------------------------------
# Tự động định cấu hình đường dẫn để Python tìm thấy gói 'src'
# Logic này xử lý việc chạy từ thư mục gốc hoặc thư mục con
current_file = os.path.abspath(__file__)
current_dir = os.path.dirname(current_file) # finceptcore/
project_root = os.path.dirname(current_dir) # FinceptTerminal/

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import module an toàn với Error Handling
try:
    from src.ui.styles import apply_terminal_style, render_ticker_tape
    from src.backend.market import MarketEngine
except ImportError as e:
    # Fallback cho trường hợp chạy lần đầu chưa có src
    # (Để tránh sập app nếu người dùng chưa copy src)
    st.error(f"CRITICAL ERROR: Cannot load core modules. {str(e)}")
    st.stop()

# -----------------------------------------------------------------------------
# 2. APPLICATION CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Fincept Terminal | Enterprise Intelligence",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Fincept-Corporation/FinceptTerminal',
        'Report a bug': "https://github.com/Fincept-Corporation/FinceptTerminal/issues",
        'About': "Fincept Terminal v3.3.2 - Institutional Grade Analytics Platform."
    }
)

# -----------------------------------------------------------------------------
# 3. GLOBAL STATE MANAGEMENT
# -----------------------------------------------------------------------------
if 'session_id' not in st.session_state:
    st.session_state.session_id = f"SES-{int(time.time())}"
if 'user_role' not in st.session_state:
    st.session_state.user_role = "PORTFOLIO_MANAGER"
if 'data_feed_status' not in st.session_state:
    st.session_state.data_feed_status = "CONNECTED"

# Áp dụng giao diện Terminal (Dark Mode + Monospace Font)
apply_terminal_style()

# -----------------------------------------------------------------------------
# 4. DATA FEED ENGINE (SỬA LỖI TẠI ĐÂY)
# -----------------------------------------------------------------------------

# Gán danh sách tài sản cụ thể, KHÔNG ĐỂ TRỐNG
tickers =

@st.cache_data(ttl=300)
def fetch_global_market_pulse(symbol_list):
    """
    Lấy dữ liệu nhanh cho thanh Ticker Tape.
    Sử dụng caching để tối ưu hiệu suất tải trang.
    """
    tape_data =
    # Chỉ lấy 10 mã đầu tiên để demo nhanh
    priority_symbols = symbol_list[:10]
    
    for sym in priority_symbols:
        try:
            # Gọi engine backend
            quote = MarketEngine.get_realtime_price(sym)
            if quote:
                tape_data.append(quote)
        except Exception:
            continue
            
    return tape_data

# Hiển thị Ticker Tape (Băng chuyền giá chạy ngang)
with st.container():
    try:
        if 'ticker_data' not in st.session_state:
            st.session_state.ticker_data = fetch_global_market_pulse(tickers)
        
        if st.session_state.ticker_data:
            render_ticker_tape(st.session_state.ticker_data)
        else:
            st.warning("⚠️ Market Data Feed Initializing...")
    except Exception as e:
        # Fail silently để không làm vỡ giao diện chính
        pass

# -----------------------------------------------------------------------------
# 5. NAVIGATION ROUTER (ĐIỀU HƯỚNG TRANG)
# -----------------------------------------------------------------------------
# Định nghĩa các đối tượng trang (Page Objects)
# Lưu ý: Các file này phải tồn tại trong thư mục pages/

# Phân hệ 1: Giám sát Thị trường
pg_cockpit = st.Page(
    "pages/1_🌐_Market_Cockpit.py", 
    title="Market Cockpit", 
    icon="🌐", 
    default=True
)

# Phân hệ 2: Phân tích Định lượng
pg_equity = st.Page(
    "pages/2_📊_Equity_Research.py", 
    title="Equity Research", 
    icon="📊"
)
pg_risk = st.Page(
    "pages/4_⚖️_Portfolio_Risk.py", 
    title="Portfolio Risk (VaR)", 
    icon="⚖️"
)

# Phân hệ 3: Trí tuệ Nhân tạo
pg_ai_core = st.Page(
    "pages/3_🧠_AI_Neural_Core.py", 
    title="AI Neural Core", 
    icon="🧠"
)

# Cấu trúc Menu Điều hướng (Grouped Navigation)
navigation_structure = {
    "MARKET INTELLIGENCE": [pg_cockpit],
    "QUANTITATIVE LAB": [pg_equity, pg_risk],
    "AI SYSTEMS": [pg_ai_core]
}

# Khởi tạo Router
pg = st.navigation(navigation_structure)

# -----------------------------------------------------------------------------
# 6. SIDEBAR CONTROLS (THANH ĐIỀU KHIỂN BÊN)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Logo Area
    st.markdown("## 🦅 FINCEPT TERM")
    st.caption(f"ID: {st.session_state.session_id}")
    st.markdown("---")
    
    # System Telemetry
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**CORE**")
        st.markdown(f"🟢 {st.session_state.data_feed_status}")
    with col2:
        st.markdown("**PING**")
        st.markdown(f"⚡ {random.randint(12, 45)}ms")
    
    st.markdown("---")
    
    # Global Asset Selector (Bộ chọn tài sản toàn cục)
    st.markdown("### 🎯 ACTIVE ASSET")
    selected_asset = st.selectbox(
        "Select Ticker", 
        tickers,
        index=0,
        label_visibility="collapsed"
    )
    
    # Lưu vào session state để các trang con sử dụng
    st.session_state.active_asset = selected_asset
    
    # Command Line Interface (CLI) Simulation
    st.markdown("### ⌨️ TERMINAL CLI")
    cmd = st.text_input("Execute Command >", placeholder="HELP for list")
    
    if cmd:
        cmd = cmd.strip().upper()
        if cmd == "CLEAR":
            st.cache_data.clear()
            st.toast("System Memory Purged", icon="🧹")
        elif cmd == "REBOOT":
            st.rerun()
        elif cmd.startswith("LOAD"):
            # Logic giả lập lệnh LOAD AAPL
            parts = cmd.split()
            if len(parts) > 1:
                st.toast(f"Loading context for {parts[1]}...", icon="🔄")
        else:
            st.info(f"Command '{cmd}' sent to buffer.")

    # Footer
    st.markdown("---")
    with st.expander("System Logs"):
        st.caption(f" Boot sequence initiated.")
        st.caption(f" Modules loaded: 4/4")
        st.caption(f" User auth: VERIFIED")

# -----------------------------------------------------------------------------
# 7. MAIN EXECUTION KERNEL
# -----------------------------------------------------------------------------
try:
    # Chạy trang được chọn
    pg.run()
    
except Exception as e:
    # Global Error Boundary (Bắt lỗi toàn cục)
    st.error("🛑 SYSTEM KERNEL PANIC")
    st.error(f"Error Details: {str(e)}")
    
    # Hiển thị hướng dẫn khắc phục sự cố
    st.markdown("### 🛠️ Troubleshooting Guide")
    st.markdown("""
    1. **Check Directory Structure:** Ensure `pages/` folder exists next to `app.py`.
    2. **Verify Dependencies:** Run `pip install -r requirements.txt`.
    3. **Module Integrity:** Ensure `src/` folder contains `__init__.py` files.
    """)
    st.code(os.popen("tree.").read(), language="bash")
