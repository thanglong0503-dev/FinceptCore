import streamlit as st
import plotly.graph_objects as go
from utils.data_fetcher import MarketDataEngine
import pandas as pd

st.title("🌐 Tổng Quan Thị Trường Toàn Cầu")

# 1. Ticker Tape (Pure HTML/CSS Injection) - [14]
# Hiển thị các chỉ số chính chạy ngang màn hình
indices =
tape_html = "<div class='ticker-wrap'><div class='ticker'>"

for ind in indices:
    q = MarketDataEngine.get_realtime_quote(ind)
    if q:
        color = "ticker-up" if q['change'] >= 0 else "ticker-down"
        symbol = "▲" if q['change'] >= 0 else "▼"
        display_name = ind.replace("^", "").replace("=X", "")
        tape_html += f"<div class='ticker-item'>{display_name}: <span class='{color}'>{q['price']:.2f} {symbol} {q['pct_change']:.2f}%</span></div>"

tape_html += "</div></div>"
st.markdown(tape_html, unsafe_allow_html=True)

st.divider()

# 2. Bảng điều khiển chính (Main Dashboard Grid)
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader(f"Biểu đồ Kỹ thuật: {st.session_state.current_ticker}")
    
    # Lấy dữ liệu 1 năm để vẽ biểu đồ
    data = MarketDataEngine.get_historical_data(st.session_state.current_ticker, period="1y", interval="1d")
    
    if not data.empty:
        # Sử dụng Plotly Graph Objects cho biểu đồ nến chuyên nghiệp [22]
        fig = go.Figure()
        
        # Nến Nhật (Candlestick)
        fig.add_trace(go.Candlestick(x=data.index,
                        open=data['Open'], high=data['High'],
                        low=data['Low'], close=data['Close'],
                        name='Price'))
        
        # Đường Bollinger Bands (được tính từ data_fetcher)
        if 'BBL_5_2.0' in data.columns and 'BBU_5_2.0' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='gray', width=1, dash='dot'), name='Upper BB'))
            fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='gray', width=1, dash='dot'), name='Lower BB', fill='tonexty'))

        # Moving Averages
        if 'SMA_50' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='cyan', width=1.5), name='SMA 50'))
        if 'SMA_200' in data.columns:
            fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='orange', width=1.5), name='SMA 200'))

        fig.update_layout(
            template="plotly_dark",
            height=600,
            xaxis_rangeslider_visible=False,
            margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Volume Chart (Biểu đồ con)
        # Có thể thêm vào đây nếu cần chi tiết hơn
    else:
        st.warning("Không có dữ liệu lịch sử.")

with col2:
    st.subheader("Chỉ Số Cơ Bản (Key Metrics)")
    quote = MarketDataEngine.get_realtime_quote(st.session_state.current_ticker)
    fund = MarketDataEngine.get_fundamental_info(st.session_state.current_ticker)
    
    if quote:
        # Hiển thị giá lớn
        st.metric("Giá Hiện tại", f"{quote['price']:.2f}", f"{quote['change']:.2f} ({quote['pct_change']:.2f}%)")
        st.metric("Khối lượng GD", f"{quote['volume']:,}")
        
    if fund and 'info' in fund:
        info = fund['info']
        st.markdown("### Hồ sơ Doanh nghiệp")
        
        # Bảng chỉ số định giá
        metrics_df = pd.DataFrame({
            "Metric":,
            "Value":
        })
        st.table(metrics_df)
        
        # Thông tin mô tả công ty
        with st.expander("Mô tả Kinh doanh"):
            st.write(info.get('longBusinessSummary', 'Không có mô tả.'))

# 3. Bản đồ Nhiệt Ngành (Sector Performance - Market Breadth)
st.subheader("Hiệu Suất Theo Ngành (Sector Heatmap)")
sectors = {
    "Công Nghệ (XLK)": "XLK", "Y Tế (XLV)": "XLV", "Tài Chính (XLF)": "XLF", 
    "Năng Lượng (XLE)": "XLE", "Tiêu Dùng (XLY)": "XLY", "Bất Động Sản (XLRE)": "XLRE"
}
cols = st.columns(len(sectors))
for i, (sec_name, sec_ticker) in enumerate(sectors.items()):
    sec_q = MarketDataEngine.get_realtime_quote(sec_ticker)
    if sec_q:
        cols[i].metric(sec_name.split(' ('), f"{sec_q['pct_change']:.2f}%", delta_color="normal")
