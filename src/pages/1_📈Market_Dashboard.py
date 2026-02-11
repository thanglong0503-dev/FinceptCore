# pages/1_📈_Market_Dashboard.py
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from src.backend.market_data import MarketDataEngine
from src.analytics.technical import TechnicalAnalyzer

st.title("Market Cockpit 📈")

# 1. Thanh điều khiển (Control Bar)
col1, col2, col3 = st.columns()
with col1:
    ticker = st.text_input("Mã Chứng Khoán (Ticker)", value="AAPL").upper()
with col2:
    period = st.selectbox("Khung Thời Gian", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)
with col3:
    st.write("") # Spacer

# 2. Hiển thị thông tin giá realtime
quote = MarketDataEngine.fetch_real_time_quote(ticker)
if quote:
    m1, m2, m3 = st.columns(3)
    m1.metric("Giá Hiện Tại", f"${quote['price']:.2f}", f"{quote['pct_change']:.2f}%")
    m2.metric("Khối Lượng", f"{quote['volume']:,}")
    m3.metric("Đóng Cửa Phiên Trước", f"${quote['previous_close']:.2f}")

# 3. Biểu đồ Phân tích Kỹ thuật
data = MarketDataEngine.fetch_historical_ohlcv(ticker, period=period)

if not data.empty:
    # Tính toán chỉ báo
    data = TechnicalAnalyzer.calculate_indicators(data)
    
    # Vẽ biểu đồ phức hợp (Subplots)
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.03, subplot_titles=(f'{ticker} Price', 'RSI'),
                        row_width=[0.2, 0.7])

    # Biểu đồ giá (Candlestick)
    fig.add_trace(go.Candlestick(x=data.index, open=data['Open'], high=data['High'],
                                 low=data['Low'], close=data['Close'], name='OHLC'), row=1, col=1)

    # Thêm đường trung bình động (MA)
    fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='orange', width=1), name='SMA 50'), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='blue', width=1), name='SMA 200'), row=1, col=1)
    
    # Thêm Bollinger Bands
    fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='gray', width=0), showlegend=False), row=1, col=1)
    fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='gray', width=0), fill='tonexty', showlegend=False), row=1, col=1)

    # Biểu đồ RSI
    fig.add_trace(go.Scatter(x=data.index, y=data, line=dict(color='purple', width=2), name='RSI'), row=2, col=1)
    # Đường tham chiếu RSI
    fig.add_hline(y=70, line_dash="dash", line_color="red", row=2, col=1)
    fig.add_hline(y=30, line_dash="dash", line_color="green", row=2, col=1)

    # Tùy chỉnh Layout
    fig.update_layout(height=800, xaxis_rangeslider_visible=False, template="plotly_dark")
    st.plotly_chart(fig, use_container_width=True)
    
    # 4. Hiển thị dữ liệu thô
    with st.expander("Xem dữ liệu lịch sử chi tiết"):
        st.dataframe(data.sort_index(ascending=False))
else:
    st.error("Không tìm thấy dữ liệu lịch sử cho mã này.")
