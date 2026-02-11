"""
FinceptTerminal v3.0 - Main Application Entry Point
---------------------------------------------------
Author: Fincept Corporation Architecture Team
Version: 3.2.1 Enterprise
License: Proprietary / Enterprise
Description: 
    Đây là tệp thực thi gốc (root execution file) cho FinceptTerminal.
    Nó chịu trách nhiệm:
    1. Cấu hình trang toàn cục (Layout, Title, Icons).
    2. Tiêm CSS/Asset tùy chỉnh (Giao diện Terminal chuẩn Bloomberg).
    3. Khởi tạo trạng thái phiên (Authentication, User Settings).
    4. Định tuyến điều hướng động (Khắc phục lỗi cú pháp dictionary cũ).
"""

import streamlit as st
import time
from datetime import datetime
import os
import sys

# Đảm bảo đường dẫn module được nhận diện
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# -----------------------------------------------------------------------------
# 1. Cấu hình Hệ thống (System Configuration)
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Fincept Terminal | Institutional Grade Analytics",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 2. Quản lý Trạng thái Phiên (Session State Management)
# -----------------------------------------------------------------------------
# Khởi tạo các biến toàn cục để duy trì trạng thái giữa các lần tải lại trang
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False  # Trạng thái đăng nhập
if 'user_role' not in st.session_state:
    st.session_state.user_role = 'guest'    # Phân quyền: guest, analyst, fund_manager
if 'current_ticker' not in st.session_state:
    st.session_state.current_ticker = "SPY" # Mã cổ phiếu mặc định
if 'theme' not in st.session_state:
    st.session_state.theme = 'Bloomberg_Dark'

# -----------------------------------------------------------------------------
# 3. Tùy chỉnh CSS & Giao diện Terminal (The "International Pro" Look)
# -----------------------------------------------------------------------------
def load_custom_css():
    """
    Tiêm CSS chuyên nghiệp để ghi đè giao diện mặc định của Streamlit.
    Mục tiêu: Chế độ tối tương phản cao, phông chữ đơn cách (monospace) cho dữ liệu.
    Tham chiếu kỹ thuật: 
    """
    st.markdown("""
        <style>
        /* Import Font: IBM Plex Mono cho dữ liệu tài chính & Inter cho UI */
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=Inter:wght@400;600&display=swap');

        /* Global Reset & Dark Mode Base */
       .stApp {
            background-color: #0e1117; /* Màu nền than chì đậm */
            color: #e0e0e0;
            font-family: 'Inter', sans-serif;
        }

        /* Metric Containers - Thẻ chỉ số tài chính */
        div[data-testid="stMetric"] {
            background-color: #1a1c24;
            padding: 15px;
            border-radius: 5px;
            border-left: 4px solid #ff4b4b; /* Điểm nhấn mặc định */
            box-shadow: 0 4px 6px rgba(0,0,0,0.3);
            transition: transform 0.2s;
        }
        div[data-testid="stMetric"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 8px rgba(0,0,0,0.4);
        }

        /* Ticker Tape Animation - Băng chuyền giá cổ phiếu [14] */
       .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background-color: #000000;
            padding-top: 10px;
            padding-bottom: 10px;
            white-space: nowrap;
            border-bottom: 1px solid #333;
            border-top: 1px solid #333;
        }
       .ticker {
            display: inline-block;
            animation: ticker-move 60s linear infinite;
        }
       .ticker-item {
            display: inline-block;
            padding: 0 2rem;
            font-family: 'IBM Plex Mono', monospace;
            font-size: 14px;
            font-weight: 600;
        }
       .ticker-up { color: #00ff00; }
       .ticker-down { color: #ff0000; }
        
        @keyframes ticker-move {
            0% { transform: translate3d(0, 0, 0); }
            100% { transform: translate3d(-100%, 0, 0); }
        }

        /* Sidebar Styling - Thanh điều hướng bên trái */
        section {
            background-color: #000000;
            border-right: 1px solid #333;
        }
        
        /* Headers & Typography */
        h1, h2, h3 {
            font-family: 'Inter', sans-serif;
            letter-spacing: -0.5px;
            color: #ffffff;
        }
        
        /* Custom Button Styling */
        div.stButton > button {
            background-color: #2c2f38;
            color: white;
            border: 1px solid #4a4e5a;
        }
        div.stButton > button:hover {
            border-color: #00ff00;
            color: #00ff00;
        }
        </style>
    """, unsafe_allow_html=True)

load_custom_css()

# -----------------------------------------------------------------------------
# 4. Cơ chế Xác thực & Bảo mật (Authentication Gatekeeper)
# -----------------------------------------------------------------------------
def login_screen():
    """
    Giao diện đăng nhập mô phỏng. Trong môi trường production, 
    cần tích hợp LDAP, OAuth2 hoặc SSO. 
    """
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("🔐 Fincept Terminal Access")
        st.markdown("---")
        st.info("Hệ thống yêu cầu xác thực cấp độ tổ chức.")
        
        username = st.text_input("Terminal ID (Default: admin)")
        password = st.text_input("Secure Key (Default: admin)", type="password")
        
        if st.button("Authenticate", type="primary", use_container_width=True):
            if username == "admin" and password == "admin":
                st.session_state.authenticated = True
                st.session_state.user_role = "Portfolio Manager"
                st.toast("Đăng nhập thành công! Đang khởi tạo kết nối vệ tinh...", icon="🛰️")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Thông tin xác thực không hợp lệ. Truy cập bị từ chối.")

# -----------------------------------------------------------------------------
# 5. Kiến trúc Điều hướng (Navigation Architecture) - Khắc phục lỗi [6]
# -----------------------------------------------------------------------------
def main_navigation():
    """
    Định nghĩa cấu trúc đa trang sử dụng st.navigation (Streamlit 1.36+).
    Phân nhóm các trang theo chức năng nghiệp vụ để mô phỏng các tab trên Bloomberg Terminal.
    """
    
    # Định nghĩa Đối tượng Trang (Page Objects)
    # Lưu ý: Các đường dẫn này giả định cấu trúc thư mục: finceptcore/pages/
    
    # Nhóm 1: Thông tin Thị trường (Market Intelligence)
    pg_market_overview = st.Page("pages/1_market_overview.py", title="Tổng Quan Thị Trường", icon="🌐", url_path="market")
    pg_forex = st.Page("pages/2_forex_commodities.py", title="Ngoại Hối & Hàng Hóa", icon="💱", url_path="forex")
    pg_macro = st.Page("pages/3_macro_economics.py", title="Dữ Liệu Vĩ Mô (DBNomics)", icon="🏛️", url_path="macro")

    # Nhóm 2: Nghiên cứu Cổ phiếu (Equity Research)
    pg_technical = st.Page("pages/4_technical_analysis.py", title="Phân Tích Kỹ Thuật", icon="📊", url_path="technical")
    pg_fundamental = st.Page("pages/5_fundamental_analysis.py", title="Phân Tích Cơ Bản", icon="📑", url_path="fundamental")
    pg_valuation = st.Page("pages/6_valuation_models.py", title="Mô Hình Định Giá DCF", icon="🧮", url_path="valuation")

    # Nhóm 3: Chiến lược & Rủi ro (Quantitative Strategy)
    pg_portfolio = st.Page("pages/7_portfolio_manager.py", title="Quản Trị Rủi Ro (VaR)", icon="🛡️", url_path="risk")
    pg_ai_agent = st.Page("pages/8_ai_consultant.py", title="Hội Đồng Đầu Tư AI", icon="🤖", url_path="ai-council")

    # Nhóm 4: Hệ thống (System)
    pg_settings = st.Page("pages/9_settings.py", title="Cấu Hình Terminal", icon="⚙️", url_path="config")

    # FIX LỖI CÚ PHÁP: Sử dụng dictionary để nhóm trang thay vì cấu trúc lỗi thời
    pages = {
        "Market Intelligence": [pg_market_overview, pg_forex, pg_macro],
        "Equity Research": [pg_technical, pg_fundamental, pg_valuation],
        "Quantitative Strategy": [pg_portfolio, pg_ai_agent],
        "System Configuration": [pg_settings]
    }

    # Khởi tạo Điều hướng
    pg = st.navigation(pages)
    
    # Sidebar Global Elements - Hiển thị thông tin trạng thái hệ thống
    with st.sidebar:
        st.markdown("## FINCEPT TERMINAL")
        st.caption(f"User: **{st.session_state.user_role}**")
        st.caption(f"Status: **Connected** 🟢")
        st.caption(f"Latency: **{int(time.time() % 1 * 50)}ms**")
        
        # Global Ticker Selector - Ô nhập mã lệnh toàn cục
        st.divider()
        st.markdown("### Command Line")
        new_ticker = st.text_input("Ticker / Command", value=st.session_state.current_ticker).upper()
        
        if new_ticker!= st.session_state.current_ticker:
            st.session_state.current_ticker = new_ticker
            st.toast(f"Đang chuyển hướng dữ liệu sang: {new_ticker}")
            st.rerun()
            
    # Thực thi trang đã chọn
    pg.run()

# -----------------------------------------------------------------------------
# 6. Kiểm soát Thực thi (Execution Control)
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    if st.session_state.authenticated:
        main_navigation()
    else:
        login_screen()
