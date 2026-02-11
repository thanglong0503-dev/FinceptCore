import yfinance as yf
import pandas as pd
import pandas_ta as ta  # Thư viện Phân tích Kỹ thuật chuyên sâu
import streamlit as st
from datetime import datetime, timedelta
import requests
import numpy as np

class MarketDataEngine:
    """
    Công cụ tìm kiếm dữ liệu tập trung cho FinceptTerminal.
    Xử lý bộ nhớ đệm (caching), phục hồi lỗi và chuẩn hóa dữ liệu.
    """
    
    @staticmethod
    @st.cache_data(ttl=60)  # Cache trong 60 giây để tạo cảm giác thời gian thực
    def get_realtime_quote(ticker: str):
        """
        Lấy dữ liệu giá mới nhất kèm theo giá đóng cửa phiên trước để tính toán delta.
        Sử dụng yf.Ticker để truy xuất dữ liệu intraday.
        """
        try:
            stock = yf.Ticker(ticker)
            # Lấy dữ liệu 5 ngày để đảm bảo có giá đóng cửa phiên trước
            hist = stock.history(period="5d", interval="1m")
            if hist.empty:
                return None
            
            latest = hist.iloc[-1]
            # Lấy giá đóng cửa phiên trước từ info hoặc tính toán từ lịch sử
            prev_close = stock.info.get('previousClose', hist.iloc['Close'])
            
            # Xử lý trường hợp giá bị NaN
            if pd.isna(prev_close):
                prev_close = hist.iloc[-2]['Close'] if len(hist) > 1 else latest['Close']
            
            return {
                'symbol': ticker,
                'price': latest['Close'],
                'open': latest['Open'],
                'high': latest['High'],
                'low': latest['Low'],
                'volume': latest['Volume'],
                'prev_close': prev_close,
                'change': latest['Close'] - prev_close,
                'pct_change': ((latest['Close'] - prev_close) / prev_close) * 100
            }
        except Exception as e:
            # Ghi log lỗi nhưng không làm sập ứng dụng
            print(f"Data Feed Error for {ticker}: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=3600)  # Cache trong 1 giờ cho dữ liệu lịch sử
    def get_historical_data(ticker: str, period: str = "2y", interval: str = "1d"):
        """
        Lấy dữ liệu OHLCV lịch sử và tự động tính toán các chỉ báo kỹ thuật cơ bản.
        Tích hợp Pandas-TA để tính RSI, MACD, Bollinger Bands ngay tại nguồn.
        Tham chiếu: [17, 18]
        """
        try:
            # Tắt thanh tiến trình để không làm rối giao diện Streamlit
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            if df.empty:
                return pd.DataFrame()
            
            # Chuẩn hóa tên cột (YFinance trả về MultiIndex trong phiên bản mới)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = [c for c in df.columns]
            
            # Tính toán Chỉ báo Kỹ thuật (Technical Indicators)
            # 1. RSI (Relative Strength Index)
            df.ta.rsi(length=14, append=True)
            # 2. MACD (Moving Average Convergence Divergence)
            df.ta.macd(append=True)
            # 3. Bollinger Bands
            df.ta.bbands(append=True)
            # 4. Moving Averages (SMA/EMA)
            df.ta.sma(length=50, append=True)
            df.ta.sma(length=200, append=True)
            
            # Loại bỏ các hàng có giá trị NaN do tính toán chỉ báo
            df.dropna(inplace=True)
            
            return df
        except Exception as e:
            st.error(f"Lỗi tải dữ liệu lịch sử: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    @st.cache_data(ttl=86400)  # Cache 24h cho dữ liệu cơ bản (Financials)
    def get_fundamental_info(ticker: str):
        """
        Lấy Bảng cân đối kế toán, Báo cáo thu nhập và Hồ sơ công ty.
        Dữ liệu này rất quan trọng cho module Định giá DCF.
        """
        try:
            stock = yf.Ticker(ticker)
            return {
                'info': stock.info,
                'balance_sheet': stock.balance_sheet,
                'income_stmt': stock.financials,
                'cashflow': stock.cashflow,
                'calendar': stock.calendar,
                'recommendations': stock.recommendations
            }
        except Exception as e:
            return None

class EconomicDataEngine:
    """
    Bộ kết nối (Connector) cho DBNomics để lấy các chỉ số Kinh tế Vĩ mô.
    Hỗ trợ GDP, CPI, Lạm phát, Lãi suất từ IMF, World Bank, OECD.
    Tham chiếu: 
    """
    
    BASE_URL = "https://api.db.nomics.world/v22"

    @staticmethod
    @st.cache_data(ttl=86400)
    def fetch_series(provider_code, dataset_code, series_code):
        """
        Hàm generic để gọi API DBNomics.
        Ví dụ: IMF/CPI/A.US.PCPIT_IX (CPI Hoa Kỳ hàng năm)
        """
        url = f"https://api.db.nomics.world/v22/series/{provider_code}/{dataset_code}/{series_code}?observations=1"
        try:
            response = requests.get(url)
            data = response.json()
            series_data = data['series']['docs']
            periods = series_data['period']
            values = series_data['value']
            
            df = pd.DataFrame({'Date': periods, 'Value': values})
            df = pd.to_datetime(df)
            df.set_index('Date', inplace=True)
            return df.sort_index()
        except Exception as e:
            st.warning(f"Dữ liệu vĩ mô không khả dụng: {str(e)}")
            return pd.DataFrame()
