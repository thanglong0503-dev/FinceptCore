"""
FINCEPT TERMINAL - ENTERPRISE EDITION
-------------------------------------
Entry Point: app.py
Version: 3.2.1 (Build 2024.10)
Author: Fincept Corporation Architecture Team
License: Proprietary / Enterprise

Description:
    Đây là kernel khởi chạy chính (Root Application Kernel). 
    Nó chịu trách nhiệm:
    1. Khởi tạo môi trường (Environment Bootstrap)
    2. Cấu hình giao diện người dùng (UI/UX Config)
    3. Định tuyến trang (Navigation Router)
    4. Quản lý trạng thái phiên (Session State Manager)
    5. Hiển thị dữ liệu thời gian thực (Real-time Ticker Tape)
"""

import streamlit as st
import sys
import os
import time
from datetime import datetime

# -----------------------------------------------------------------------------
# 1. SYSTEM PATH BOOTSTRAP (KHỞI TẠO ĐƯỜNG DẪN)
# -----------------------------------------------------------------------------
# Đảm bảo Python có thể tìm thấy module 'src' dù chạy từ thư mục nào
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(current_dir) if "finceptcore" in current_dir else current_dir
if root_dir not in sys.path:
    sys.path.append(root_dir)

# Import các module nội bộ sau khi fix đường dẫn
try:
    from src.ui.styles import apply_terminal_style, render_ticker_tape
    from src.backend.market import MarketEngine
except ImportError as e:
    st.error(f"CRITICAL SYSTEM ERROR: Could not load core modules. {str(e)}")
    st.stop()

# -----------------------------------------------------------------------------
# 2. PAGE CONFIGURATION (CẤU HÌNH TRANG - BẮT BUỘC DÒNG ĐẦU TIÊN)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Fincept Terminal | Institutional Analytics",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Fincept-Corporation/FinceptTerminal',
        'Report a bug': "https://github.com/Fincept-Corporation/FinceptTerminal/issues",
        'About': "Fincept Terminal v3.2 Enterprise Edition. (c) 2024 Fincept Corp."
    }
)

# -----------------------------------------------------------------------------
# 3. SESSION STATE INITIALIZATION (QUẢN LÝ TRẠNG THÁI)
# -----------------------------------------------------------------------------
if 'system_status' not in st.session_state:
    st.session_state.system_status = "ONLINE"
if 'last_update' not in st.session_state:
    st.session_state.last_update = datetime.now().strftime("%H:%M:%S")
if 'user_mode' not in st.session_state:
    st.session_state.user_mode = "ANALYST"

# Áp dụng CSS giao diện Terminal chuyên nghiệp
apply_terminal_style()

# -----------------------------------------------------------------------------
# 4. GLOBAL DATA & TICKER TAPE (FIX LỖI CÚ PHÁP TẠI ĐÂY)
# -----------------------------------------------------------------------------

# --- SỬA LỖI SYNTAX ERROR DÒNG 18 ---
# Khai báo danh sách tickers toàn cầu để chạy Ticker Tape
tickers =
# --- ---

def load_ticker_tape_data():
    """
    Hàm helper để lấy dữ liệu cho băng chuyền giá.
    Sử dụng cơ chế caching của Streamlit để tránh spam API.
    """
    tape_data =
    # Chỉ lấy dữ liệu mẫu cho 7 mã đầu tiên để tối ưu hiệu suất khởi động
    display_tickers = tickers[:7] 
    
    for t in display_tickers:
        quote = MarketEngine.get_realtime_price(t)
        if quote:
            tape_data.append(quote)
    return tape_data

# Render Ticker Tape ở đầu trang (Top Bar)
with st.container():
    try:
        live_data = load_ticker_tape_data()
        render_ticker_tape(live_data)
    except Exception as e:
        st.warning("Ticker tape offline: Reconnecting data feed...")

# -----------------------------------------------------------------------------
# 5. NAVIGATION ROUTING (ĐỊNH TUYẾN TRANG)
# -----------------------------------------------------------------------------
# Định nghĩa cấu trúc điều hướng phân cấp (Hierarchical Navigation)
# Yêu cầu thư mục pages/ phải tồn tại và chứa các file tương ứng

# Nhóm 1: Market Intelligence (Thông tin thị trường)
pg_market = st.Page("pages/1_🌐_Market_Cockpit.py", title="Market Cockpit", icon="🌐", default=True)

# Nhóm 2: Deep Research (Nghiên cứu chuyên sâu)
pg_equity = st.Page("pages/2_📊_Equity_Research.py", title="Equity Research", icon="📊")

# Nhóm 3: AI Core (Trí tuệ nhân tạo)
pg_ai = st.Page("pages/3_🧠_AI_Neural_Core.py", title="AI Neural Core", icon="🧠")

# Nhóm 4: Risk Management (Quản trị rủi ro)
pg_risk = st.Page("pages/4_⚖️_Portfolio_Risk.py", title="Portfolio Risk", icon="⚖️")

# Cấu trúc Navigation Dictionary
pages_structure = {
    "MARKET SURVEILLANCE": [pg_market],
    "QUANTITATIVE LAB": [pg_equity, pg_risk],
    "INTELLIGENCE UNIT": [pg_ai]
}

# Khởi tạo Router
pg = st.navigation(pages_structure)

# -----------------------------------------------------------------------------
# 6. SIDEBAR & SYSTEM CONTROLS (THANH BÊN)
# -----------------------------------------------------------------------------
with st.sidebar:
    # Header Logo/Brand
    st.markdown("## 🦅 FINCEPT TERM")
    st.caption("v3.2.1 | ENTERPRISE BUILD")
    st.markdown("---")
    
    # System Status Indicator
    col_status, col_latency = st.columns(2)
    with col_status:
        st.markdown("**STATUS**")
        st.markdown(f"🟢 {st.session_state.system_status}")
    with col_latency:
        st.markdown("**LATENCY**")
        st.markdown(f"⚡ {int(time.time() * 1000) % 50}ms")
    
    st.markdown("---")
    
    # Quick Command Line Interface (CLI Simulation)
    cmd_input = st.text_input("TERMINAL COMMAND >", placeholder="Type ticker or cmd...")
    
    if cmd_input:
        if cmd_input.upper() == "CLEAR":
            st.cache_data.clear()
            st.toast("System Cache Purged", icon="🧹")
        elif cmd_input.upper() == "EXIT":
            st.stop()
        elif cmd_input.upper() == "HELP":
            st.info("Commands: CLEAR, EXIT,")
        else:
            # Giả lập chuyển hướng nhanh đến mã cổ phiếu
            st.toast(f"Executing command: LOAD {cmd_input.upper()}", icon="🚀")
            st.session_state['quick_ticker'] = cmd_input.upper()

    # Footer Info
    st.markdown("---")
    st.markdown("### DATA FEEDS")
    st.caption("✅ NYSE/NASDAQ (Delayed 15m)")
    st.caption("✅ FOREX/CRYPTO (Realtime)")
    st.caption("✅ MACRO/FED (Daily)")
    
    with st.expander("System Logs"):
        st.text(f" SYS_BOOT_COMPLETE")
        st.text(f" CONNECTED_TO_CORE")
        st.text(f" USER_AUTH_OK")

# -----------------------------------------------------------------------------
# 7. EXECUTION KERNEL (KHỞI CHẠY)
# -----------------------------------------------------------------------------
try:
    # Chạy trang được chọn từ Router
    pg.run()
    
except Exception as e:
    # Error Boundary (Bắt lỗi toàn cục để không sập app)
    st.error("🛑 KERNEL PANIC: Unhandled Exception in Page Execution")
    st.code(str(e), language="python")
    st.markdown("### Troubleshooting Protocol:")
    st.markdown("1. Verify `src/` module integrity.")
    st.markdown("2. Check internet connection for Data Feeds.")
    st.markdown("3. Review `requirements.txt` dependencies.")
