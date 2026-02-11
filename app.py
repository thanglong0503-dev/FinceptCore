# app.py
import streamlit as st

# Cấu hình trang phải là lệnh đầu tiên
st.set_page_config(
    page_title="Fincept Terminal Clone",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS tùy chỉnh để giao diện giống "Terminal" chuyên nghiệp
def load_css():
    st.markdown("""
        <style>
       .stApp {
            background-color: #0E1117; /* Màu nền tối */
        }
        /* Tùy chỉnh Metric Card */
        div[data-testid="stMetric"] {
            background-color: #262730;
            padding: 15px;
            border-radius: 5px;
            border: 1px solid #4c4c4c;
        }
        </style>
    """, unsafe_allow_html=True)

load_css()

# Định nghĩa các trang
pages = {
    "Dashboards":,
    "Intelligence":,
    "System":
}

# Tạo thanh điều hướng
pg = st.navigation(pages)

# Thêm Logo hoặc thông tin vào Sidebar
st.sidebar.title("FINCEPT TERMINAL")
st.sidebar.info("Phiên bản Python/Streamlit v1.0")
st.sidebar.markdown("---")

# Chạy trang được chọn
pg.run()
