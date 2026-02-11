"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: app.py
ROLE: Main Entry Point & Executive Dashboard (Trung tâm Chỉ huy)
AUTHOR: Fincept Copilot (Emo)
STANDARD: Enterprise Grade - Modular Architecture
=============================================================================
"""

import streamlit as st
import datetime
import time
import os
import sys

# ---------------------------------------------------------------------------
# 1. THIẾT LẬP MÔI TRƯỜNG & ĐƯỜNG DẪN (SYSTEM PATH)
# ---------------------------------------------------------------------------
# Đảm bảo Python có thể đọc được các module trong thư mục 'src'
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT_DIR)

# ---------------------------------------------------------------------------
# 2. CẤU HÌNH TRANG (PAGE CONFIG) - Phải là lệnh Streamlit đầu tiên
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Fincept Terminal | Command Center",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# 3. CSS TÙY CHỈNH (INLINE TERMINAL STYLE)
# ---------------------------------------------------------------------------
def inject_custom_css():
    """Bơm CSS để ép giao diện thành chuẩn Bloomberg Terminal"""
    st.markdown("""
        <style>
            /* Định dạng font chữ Monospace cho toàn hệ thống */
            html, body, [class*="css"] {
                font-family: 'Roboto Mono', 'Courier New', Courier, monospace !important;
            }
            
            /* Định dạng tiêu đề vệt sáng Neon */
            h1, h2, h3 {
                color: #00FFAA !important;
                text-shadow: 0px 0px 5px rgba(0, 255, 170, 0.3);
                letter-spacing: -0.5px;
            }
            
            /* Định dạng thẻ Metric (Chỉ số) */
            div[data-testid="stMetricValue"] {
                color: #FFFFFF !important;
                font-size: 1.8rem !important;
                font-weight: bold;
            }
            div[data-testid="stMetricLabel"] {
                color: #8892B0 !important;
                font-size: 0.9rem !important;
                text-transform: uppercase;
                letter-spacing: 1px;
            }
            
            /* Ẩn bớt các thành phần rườm rà của Streamlit mặc định */
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            
            /* Box chẩn đoán hệ thống */
            .system-box {
                border: 1px solid #262730;
                border-radius: 5px;
                padding: 15px;
                background-color: #11141A;
            }
        </style>
    """, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# 4. HIỆU ỨNG KHỞI ĐỘNG HỆ THỐNG (BOOT SEQUENCE)
# ---------------------------------------------------------------------------
def terminal_boot_sequence():
    """Hiệu ứng chạy text giả lập quá trình khởi động máy chủ"""
    if 'system_booted' not in st.session_state:
        boot_placeholder = st.empty()
        with boot_placeholder.container():
            st.markdown("### 🦅 FINCEPT BIOS v3.0.1 INITIALIZING...")
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            # Giả lập quá trình load modules
            boot_logs = [
                "Mounting secure volumes...",
                "Loading Fincept Quant Engine...",
                "Connecting to Global Market Data APIs...",
                "Initializing Neural Core Agents...",
                "Establishing secure connection to CFA Risk Module...",
                "Decrypting user session...",
                "System Ready."
            ]
            
            for i, log in enumerate(boot_logs):
                status_text.code(f"[{datetime.datetime.now().strftime('%H:%M:%S.%f')[:-3]}] {log}", language="bash")
                progress_bar.progress((i + 1) * (100 // len(boot_logs)))
                time.sleep(0.3) # Độ trễ tạo cảm giác chân thực
                
            time.sleep(0.5)
        
        # Xóa hiệu ứng sau khi boot xong
        boot_placeholder.empty()
        st.session_state['system_booted'] = True

# ---------------------------------------------------------------------------
# 5. HÀM KIỂM TRA TRẠNG THÁI MODULE (SYSTEM DIAGNOSTICS)
# ---------------------------------------------------------------------------
def check_module_status(filepath: str) -> tuple[str, str]:
    """Kiểm tra xem file module đã được tạo hay chưa"""
    full_path = os.path.join(ROOT_DIR, filepath)
    if os.path.exists(full_path):
        return "ONLINE", "normal" # Xanh lá
    return "OFFLINE", "inverse"   # Đỏ

# ===========================================================================
# MAIN DASHBOARD EXECUTION
# ===========================================================================
def main():
    # 1. Kích hoạt giao diện & Hiệu ứng
    inject_custom_css()
    terminal_boot_sequence()

    # 2. Tiêu đề Dashboard
    st.title("🦅 FINCEPT TERMINAL: COMMAND CENTER")
    st.markdown("`[AUTHORIZATION: ADMIN] | [ENCRYPTION: 256-BIT AES] | [STATUS: SECURE]`")
    st.divider()

    # 3. GLOBAL CLOCK (Giờ thế giới)
    st.subheader("🌍 GLOBAL MARKET CLOCKS")
    now_utc = datetime.datetime.utcnow()
    
    col_t1, col_t2, col_t3, col_t4 = st.columns(4)
    # New York (UTC-5 / UTC-4) -> Giả định UTC-5 cho đơn giản
    col_t1.metric("NEW YORK (NYSE/NASDAQ)", (now_utc - datetime.timedelta(hours=5)).strftime("%H:%M:%S"), "EST")
    # London (UTC+0)
    col_t2.metric("LONDON (LSE)", now_utc.strftime("%H:%M:%S"), "GMT")
    # Tokyo (UTC+9)
    col_t3.metric("TOKYO (TSE)", (now_utc + datetime.timedelta(hours=9)).strftime("%H:%M:%S"), "JST")
    # Ho Chi Minh (UTC+7)
    col_t4.metric("HO CHI MINH (HOSE)", (now_utc + datetime.timedelta(hours=7)).strftime("%H:%M:%S"), "ICT")
    
    st.markdown("---")

    # 4. CHẨN ĐOÁN HỆ THỐNG (SYSTEM DIAGNOSTICS)
    st.subheader("⚙️ SYSTEM DIAGNOSTICS & NODE STATUS")
    st.info("Bảng theo dõi tiến độ lắp ráp các Module. Hệ thống sẽ tự động cập nhật khi Ngài thêm file mới.")
    
    # Kiểm tra các module Backend
    m1, m2, m3, m4 = st.columns(4)
    
    # Check Market Engine
    status_market, color_market = check_module_status("src/backend/market.py")
    m1.metric("Node: Market Data", status_market, "src/backend/market.py", delta_color=color_market)
    
    # Check Valuation Engine
    status_val, color_val = check_module_status("src/analytics/valuation.py")
    m2.metric("Node: DCF Valuation", status_val, "src/analytics/valuation.py", delta_color=color_val)
    
    # Check Risk Engine
    status_risk, color_risk = check_module_status("src/analytics/risk.py")
    m3.metric("Node: Risk & CFA", status_risk, "src/analytics/risk.py", delta_color=color_risk)
    
    # Check Neural Core
    status_ai, color_ai = check_module_status("src/backend/macro.py") # Tạm check file macro
    m4.metric("Node: AI & Macro", status_ai, "src/backend/macro.py", delta_color=color_ai)

    st.markdown("---")

    # 5. KHU VỰC THÔNG BÁO (TERMINAL LOGS)
    st.subheader("🖥️ TERMINAL LOGS")
    logs = f"""
[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYS_INFO: Command Center Access Granted.
[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYS_WARN: Some backend nodes are currently OFFLINE.
[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] ACTION_REQ: Awaiting Developer to provision 'src/backend' and 'src/analytics' modules.
[{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] GUIDANCE: Please use the Sidebar to navigate to available Multi-pages.
    """
    st.code(logs.strip(), language="bash")

if __name__ == "__main__":
    main()
