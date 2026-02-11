import streamlit as st
from src.ui.styles import apply_terminal_style, render_ticker_tape
from src.backend.market import MarketEngine

# 1. Cấu hình Trang phải là dòng đầu tiên
st.set_page_config(
    page_title="Fincept Terminal Enterprise",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Áp dụng Giao diện Terminal
apply_terminal_style()

# 3. Hiển thị Ticker Tape (Băng chuyền giá)
# Lấy dữ liệu mẫu cho tape
tickers =
tape_data = [MarketEngine.get_realtime_price(t) for t in tickers]
render_ticker_tape(tape_data)

# 4. ĐỊNH TUYẾN TRANG (NAVIGATION ROUTER)
# Khắc phục lỗi: Chỉ trỏ đến các file ĐÃ TỒN TẠI trong thư mục pages/
pg = st.navigation({
    "MARKET INTELLIGENCE":,
    "QUANTITATIVE LAB":
})

# 5. SIDEBAR INFO
with st.sidebar:
    st.image("https://placehold.co/200x50/000000/00FF41/png?text=FINCEPT+TERM", use_column_width=True)
    st.markdown("---")
    st.info("**SYSTEM STATUS:** ONLINE 🟢")
    st.caption("v3.1.0 Enterprise Build")
    
    if st.button("CLEAR CACHE"):
        st.cache_data.clear()
        st.toast("System Memory Purged", icon="🧹")

# 6. KHỞI CHẠY TRANG ĐƯỢC CHỌN
try:
    pg.run()
except Exception as e:
    st.error(f"NAVIGATION ERROR: {str(e)}")
    st.markdown("### Troubleshooting:")
    st.markdown("1. Make sure you created the `pages/` directory.")
    st.markdown("2. Make sure all Python files are inside `pages/`.")
