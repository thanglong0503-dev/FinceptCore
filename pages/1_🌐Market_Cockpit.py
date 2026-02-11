import streamlit as st
import plotly.graph_objects as go
from src.backend.market import MarketEngine
from src.analytics.technical import TechnicalEngine
from src.ui.styles import apply_terminal_style

# Áp dụng CSS
apply_terminal_style()

st.title("🌐 MARKET COCKPIT")
st.caption("Real-time Global Surveillance System")

# Sidebar Controls
ticker = st.sidebar.text_input("COMMAND LINE (Ticker)", value="BTC-USD").upper()
period = st.sidebar.selectbox("TIMEFRAME", ["1d", "5d", "1mo", "3mo", "6mo", "1y", "ytd", "max"], index=4)

# Data Fetching
data = MarketEngine.get_historical_data(ticker, period=period)
quote = MarketEngine.get_realtime_price(ticker)

# Metrics Row
c1, c2, c3, c4 = st.columns(4)
c1.metric("LAST PRICE", f"${quote['price']}", f"{quote['change']}%")
c2.metric("VOLUME", f"{quote['volume']:,}")
c3.metric("HIGH (Period)", f"${data['High'].max():.2f}" if not data.empty else "N/A")
c4.metric("LOW (Period)", f"${data['Low'].min():.2f}" if not data.empty else "N/A")

st.markdown("---")

# Charting Area
if not data.empty:
    df_tech = TechnicalEngine.calculate_core_indicators(data)
    
    fig = go.Figure()
    
    # Candlestick
    fig.add_trace(go.Candlestick(x=df_tech.index,
                                 open=df_tech['Open'], high=df_tech['High'],
                                 low=df_tech['Low'], close=df_tech['Close'],
                                 name='Price'))
    
    # SMAs
    if 'SMA_50' in df_tech.columns:
        fig.add_trace(go.Scatter(x=df_tech.index, y=df_tech, line=dict(color='orange', width=1), name='SMA 50'))
    if 'SMA_200' in df_tech.columns:
        fig.add_trace(go.Scatter(x=df_tech.index, y=df_tech, line=dict(color='blue', width=1), name='SMA 200'))
    
    # BBands
    if 'BBU_20_2.0' in df_tech.columns:
        fig.add_trace(go.Scatter(x=df_tech.index, y=df_tech, line=dict(color='gray', width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=df_tech.index, y=df_tech, line=dict(color='gray', width=0), fill='tonexty', showlegend=False))

    fig.update_layout(
        template="plotly_dark",
        height=700,
        xaxis_rangeslider_visible=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.error(f"NO DATA RECEIVED FOR {ticker}")
