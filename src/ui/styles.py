import streamlit as st

def apply_terminal_style():
    st.markdown("""
        <style>
        /* Nhập font IBM Plex Mono cho giao diện giống Terminal */
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&display=swap');
        
        html, body, [class*="css"] {
            font-family: 'IBM Plex Mono', monospace;
        }
        
        /* Tùy chỉnh thanh cuộn */
        ::-webkit-scrollbar {
            width: 8px;
            background: #0D1117;
        }
        ::-webkit-scrollbar-thumb {
            background: #30363D;
            border-radius: 4px;
        }

        /* Metrics Card Style */
        div[data-testid="stMetric"] {
            background-color: #161B22;
            border: 1px solid #30363D;
            padding: 15px;
            border-radius: 6px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: all 0.2s ease;
        }
        div[data-testid="stMetric"]:hover {
            border-color: #00FF41;
            box-shadow: 0 0 10px rgba(0, 255, 65, 0.2);
        }

        /* Ticker Tape Animation */
      .ticker-wrap {
            width: 100%;
            overflow: hidden;
            background-color: #000;
            padding: 10px 0;
            border-bottom: 1px solid #30363D;
            border-top: 1px solid #30363D;
            white-space: nowrap;
        }
      .ticker {
            display: inline-block;
            animation: ticker 60s linear infinite;
        }
      .ticker-item {
            display: inline-block;
            padding: 0 2rem;
            font-size: 14px;
            color: #00FF41;
        }
      .ticker-item.down { color: #FF4B4B; }
        
        @keyframes ticker {
            0% { transform: translateX(0); }
            100% { transform: translateX(-100%); }
        }

        /* Input Fields */
      .stTextInput > div > div > input {
            background-color: #0D1117;
            color: #00FF41;
            border: 1px solid #30363D;
        }
        </style>
    """, unsafe_allow_html=True)

def render_ticker_tape(data_list):
    """Hiển thị dải băng chạy giá cổ phiếu"""
    items_html = ""
    for item in data_list:
        color_class = "down" if item['change'] < 0 else ""
        arrow = "▼" if item['change'] < 0 else "▲"
        items_html += f"<span class='ticker-item {color_class}'>{item['symbol']} {item['price']} {arrow} {item['change']}%</span>"
    
    # Nhân đôi để tạo hiệu ứng vô tận
    html = f"""
    <div class='ticker-wrap'>
        <div class='ticker'>
            {items_html} {items_html} {items_html}
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
