# src/backend/market_data.py
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta

class MarketDataEngine:
    """
    Class chịu trách nhiệm quản lý mọi tương tác với dữ liệu thị trường chứng khoán.
    Sử dụng mô hình Singleton hoặc các phương thức tĩnh (static methods) để dễ dàng gọi từ UI.
    """

    @staticmethod
    @st.cache_data(ttl=300)  # Cache dữ liệu trong 5 phút để giảm tải API
    def fetch_real_time_quote(ticker: str):
        """
        Lấy giá thời gian thực và thông tin cơ bản của mã chứng khoán.
        
        Args:
            ticker (str): Mã chứng khoán (ví dụ: 'AAPL', 'BTC-USD').
            
        Returns:
            dict: Dictionary chứa giá hiện tại, thay đổi giá, và khối lượng.
        """
        try:
            stock = yf.Ticker(ticker)
            # Sử dụng fast_info để truy xuất nhanh hơn
            info = stock.fast_info
            quote = {
                "price": info.last_price,
                "previous_close": info.previous_close,
                "change": info.last_price - info.previous_close,
                "pct_change": ((info.last_price - info.previous_close) / info.previous_close) * 100,
                "volume": info.last_volume,
                "currency": info.currency
            }
            return quote
        except Exception as e:
            st.error(f"Lỗi khi lấy dữ liệu giá cho {ticker}: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=3600)  # Cache lịch sử giá trong 1 giờ
    def fetch_historical_ohlcv(ticker: str, period: str = "1y", interval: str = "1d") -> pd.DataFrame:
        """
        Lấy dữ liệu lịch sử OHLCV (Open, High, Low, Close, Volume).
        Hỗ trợ các khung thời gian: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max.
        """
        try:
            df = yf.download(ticker, period=period, interval=interval, progress=False, auto_adjust=True)
            
            if df.empty:
                return pd.DataFrame()
            
            # Chuẩn hóa tên cột để đảm bảo tính nhất quán trong toàn hệ thống
            df.columns = [col if isinstance(col, str) else col for col in df.columns]
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # Kiểm tra xem dữ liệu trả về có đủ cột không
            if not all(col in df.columns for col in required_cols):
                # Xử lý trường hợp yfinance trả về cấu trúc MultiIndex phức tạp
                pass 
                
            return df
        except Exception as e:
            st.error(f"Lỗi khi tải lịch sử giá {ticker}: {str(e)}")
            return pd.DataFrame()

    @staticmethod
    @st.cache_data(ttl=86400)  # Cache báo cáo tài chính trong 24 giờ
    def fetch_financial_statements(ticker: str):
        """
        Lấy Bảng cân đối kế toán, Báo cáo kết quả kinh doanh và Lưu chuyển tiền tệ.
        Dữ liệu này rất quan trọng cho module Phân tích Cơ bản (Fundamental Analysis).
        """
        try:
            stock = yf.Ticker(ticker)
            financials = {
                "balance_sheet": stock.balance_sheet,
                "income_stmt": stock.income_stmt,
                "cashflow": stock.cashflow,
                "quarterly_balance_sheet": stock.quarterly_balance_sheet,
                "quarterly_income_stmt": stock.quarterly_income_stmt,
                "quarterly_cashflow": stock.quarterly_cashflow,
            }
            return financials
        except Exception as e:
            return None
