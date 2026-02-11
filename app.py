import streamlit as st
import os
import sys

# Thêm đường dẫn để python tìm thấy module src
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from src.ui.styles import apply_terminal_style, render_ticker_tape
from src.backend.market import MarketEngine

# 1. Cấu hình Trang (Bắt buộc phải là lệnh đầu tiên)
st.set_page_config(
    page_title="Fincept Terminal Enterprise",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Áp dụng Giao diện Terminal
apply_terminal_style()

# 3. Hiển thị Ticker Tape (Băng chuyền giá)
# =========================================================================
# SỬA LỖI SYNTAX Ở DÂY: Gán list cho biến tickers
# =========================================================================
tickers =
# =========================================================================

# Lấy dữ liệu mẫu cho tape (Chỉ lấy 5 mã đầu để demo cho nhanh)
tape_data = [MarketEngine.get_realtime_price(t) for t in tickers[:5]]
render_ticker_tape(tape_data)

# 4. ĐỊNH TUYẾN TRANG (NAVIGATION ROUTER)
# Đảm bảo bạn đã tạo thư mục 'pages/' và các file bên trong như hướng dẫn
pg = st.navigation({
    "MARKET INTELLIGENCE":,
    "QUANTITATIVE LAB":
})

# 5. SIDEBAR INFO
with st.sidebar:
    st.image("https://placehold.co/200x50/000000/00FF41/png?text=FINCEPT+TERM", use_column_width=True)
    st.markdown("---")
    st.info("**SYSTEM STATUS:** ONLINE 🟢")
    st.caption("v3.2.1 Stable Build")
    
    if st.button("CLEAR CACHE"):
        st.cache_data.clear()
        st.toast("System Memory Purged", icon="🧹")

# 6. KHỞI CHẠY TRANG ĐƯỢC CHỌN
try:
    pg.run()
except Exception as e:
    st.error(f"CRITICAL BOOT ERROR: {str(e)}")
    st.markdown("### Troubleshooting:")
    st.markdown("1. Verify `pages/` directory exists.")
    st.markdown("2. Check if all python modules are correctly placed in `src/`.")
