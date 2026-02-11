"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/ui/styles.py
ROLE: Global CSS & Theming Engine
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import streamlit as st

def apply_terminal_style():
    """
    Tiêm mã CSS tùy chỉnh để ghi đè giao diện mặc định của Streamlit.
    Tạo cảm giác "Hacker/Quant" chuyên nghiệp với font Monospace.
    """
    st.markdown("""
        <style>
            /* 1. Hình nền và Font chữ tổng thể */
            .stApp {
                background-color: #0E1117;
                font-family: 'Inter', -apple-system, sans-serif;
            }
            
            /* 2. Tiêu đề - Hiệu ứng vệt sáng Neon */
            h1, h2, h3, h4, h5, h6 {
                font-family: 'Roboto Mono', 'Courier New', monospace !important;
                color: #00FFAA !important;
                letter-spacing: -0.5px;
                text-shadow: 0px 0px 8px rgba(0, 255, 170, 0.2);
            }
            
            /* 3. Thẻ Chỉ số (Metrics Card) */
            div[data-testid="stMetricValue"] {
                font-family: 'Roboto Mono', monospace;
                color: #FAFAFA !important;
                font-size: 2.2rem !important;
                font-weight: 700;
            }
            div[data-testid="stMetricLabel"] {
                font-family: 'Inter', sans-serif;
                color: #8892B0 !important;
                font-size: 0.95rem !important;
                text-transform: uppercase;
                letter-spacing: 1.5px;
            }
            div[data-testid="stMetricDelta"] svg {
                stroke-width: 3px;
            }
            
            /* 4. Khung viền và Đường chia cắt */
            hr {
                border-color: #262730;
                margin-top: 1.5rem;
                margin-bottom: 1.5rem;
            }
            
            /* 5. Nút bấm (Buttons) phong cách Cyberpunk */
            .stButton>button {
                font-family: 'Roboto Mono', monospace;
                font-weight: bold;
                border: 1px solid #00FFAA;
                color: #00FFAA;
                background-color: transparent;
                transition: all 0.3s ease;
                text-transform: uppercase;
                letter-spacing: 1px;
                width: 100%;
            }
            .stButton>button:hover {
                background-color: #00FFAA;
                color: #0E1117;
                box-shadow: 0px 0px 10px rgba(0, 255, 170, 0.4);
                border-color: #00FFAA;
            }
            
            /* 6. Bảng dữ liệu (DataFrames) */
            .stDataFrame {
                font-family: 'Roboto Mono', monospace !important;
                font-size: 0.85rem;
            }
            
            /* 7. Các ô nhập liệu (Inputs) */
            .stTextInput>div>div>input, .stNumberInput>div>div>input {
                font-family: 'Roboto Mono', monospace !important;
                color: #00FFAA !important;
                background-color: #11141A !important;
                border: 1px solid #262730 !important;
            }
            .stTextInput>div>div>input:focus, .stNumberInput>div>div>input:focus {
                border: 1px solid #00FFAA !important;
                box-shadow: 0 0 5px rgba(0, 255, 170, 0.5) !important;
            }
            
            /* 8. Ẩn menu rườm rà */
            #MainMenu {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)
