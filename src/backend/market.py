"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/backend/market.py
ROLE: Market Data Engine (Động cơ dữ liệu thị trường)
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import yfinance as yf
import pandas as pd
import numpy as np
import streamlit as st
import logging
from typing import Optional, Dict, Any, Tuple

# Thiết lập hệ thống ghi log
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MarketDataEngine:
    """
    Engine xử lý dữ liệu thị trường thời gian thực và lịch sử.
    Sử dụng Singleton pattern và Streamlit Caching để tối ưu hóa API calls.
    """

    @staticmethod
    @st.cache_data(ttl=300, show_spinner=False) # Cache 5 phút
    def get_company_info(ticker: str) -> Dict[str, Any]:
        """
        Lấy hồ sơ doanh nghiệp và các chỉ số tài chính cơ bản.
        """
        logger.info(f"FETCHING INFO: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            info = stock.info
            
            # Xử lý trường hợp ticker không hợp lệ
            if not info or 'symbol' not in info:
                return {"error": f"Ticker '{ticker}' not found or delisted."}

            return {
                "symbol": info.get("symbol", ticker),
                "name": info.get("shortName", info.get("longName", ticker)),
                "sector": info.get("sector", "N/A"),
                "industry": info.get("industry", "N/A"),
                "country": info.get("country", "N/A"),
                "currency": info.get("financialCurrency", "USD"),
                "exchange": info.get("exchange", "N/A"),
                
                # Market Metrics
                "current_price": info.get("currentPrice", info.get("regularMarketPrice", 0.0)),
                "previous_close": info.get("previousClose", 0.0),
                "open": info.get("open", 0.0),
                "day_high": info.get("dayHigh", 0.0),
                "day_low": info.get("dayLow", 0.0),
                "volume": info.get("volume", 0),
                "avg_volume_10d": info.get("averageVolume10days", 0),
                "market_cap": info.get("marketCap", 0),
                
                # Valuation Metrics
                "pe_ratio": info.get("trailingPE", info.get("forwardPE", 0.0)),
                "pb_ratio": info.get("priceToBook", 0.0),
                "ps_ratio": info.get("priceToSalesTrailing12Months", 0.0),
                "beta": info.get("beta", 1.0),
                "dividend_yield": info.get("dividendYield", 0.0),
                
                # 52 Week Data
                "fiftyTwoWeekHigh": info.get("fiftyTwoWeekHigh", 0.0),
                "fiftyTwoWeekLow": info.get("fiftyTwoWeekLow", 0.0),
                
                "summary": info.get("longBusinessSummary", "No company profile available.")
            }
        except Exception as e:
            logger.error(f"Error fetching info for {ticker}: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    @st.cache_data(ttl=300, show_spinner=False)
    def get_historical_data(ticker: str, period: str = "1y", interval: str = "1d") -> Optional[pd.DataFrame]:
        """
        Lấy dữ liệu OHLCV (Open, High, Low, Close, Volume) để vẽ biểu đồ.
        Hỗ trợ các khung thời gian: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        Hỗ trợ các interval: 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        """
        logger.info(f"FETCHING OHLCV: {ticker} | Period: {period} | Interval: {interval}")
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period, interval=interval)
            
            if df is None or df.empty:
                return None
                
            # Chuẩn hóa dữ liệu
            df.reset_index(inplace=True)
            
            # Đồng nhất tên cột thời gian thành 'timestamp'
            time_col = 'Datetime' if 'Datetime' in df.columns else 'Date'
            if time_col in df.columns:
                df.rename(columns={time_col: 'timestamp'}, inplace=True)
                
            # Loại bỏ múi giờ (timezone tz-aware) để tránh lỗi khi vẽ biểu đồ Plotly
            if pd.api.types.is_datetime64_any_dtype(df['timestamp']):
                df['timestamp'] = df['timestamp'].dt.tz_localize(None)

            # Đảm bảo các cột số liệu đúng định dạng float
            numeric_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in numeric_cols:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0.0)

            return df
        except Exception as e:
            logger.error(f"Error fetching historical data for {ticker}: {str(e)}")
            return None

    @staticmethod
    @st.cache_data(ttl=86400, show_spinner=False) # Cache 1 ngày cho BCTC
    def get_financial_statements(ticker: str) -> Dict[str, Optional[pd.DataFrame]]:
        """
        Lấy 3 báo cáo tài chính cốt lõi (cho module Định giá DCF sau này):
        1. Income Statement (Báo cáo KQKD)
        2. Balance Sheet (Bảng CĐKT)
        3. Cash Flow (Báo cáo LCTT)
        """
        logger.info(f"FETCHING FINANCIALS: {ticker}")
        try:
            stock = yf.Ticker(ticker)
            return {
                "income_statement": stock.financials,
                "balance_sheet": stock.balance_sheet,
                "cash_flow": stock.cashflow
            }
        except Exception as e:
            logger.error(f"Error fetching financials for {ticker}: {str(e)}")
            return {
                "income_statement": None,
                "balance_sheet": None,
                "cash_flow": None
            }

    @staticmethod
    def calculate_price_change(current: float, previous: float) -> Tuple[float, float]:
        """Tính toán biến động giá (Số tuyệt đối & Phần trăm)"""
        if not previous or previous == 0:
            return 0.0, 0.0
        change_abs = current - previous
        change_pct = (change_abs / previous) * 100
        return float(change_abs), float(change_pct)

    @staticmethod
    def calculate_volatility(df: pd.DataFrame, window: int = 20) -> Optional[float]:
        """Tính độ biến động lịch sử (Historical Volatility) dựa trên Log Returns"""
        if df is None or df.empty or 'Close' not in df.columns or len(df) < window:
            return None
            
        try:
            # Tính Log Returns
            log_returns = np.log(df['Close'] / df['Close'].shift(1))
            
            # Tính độ lệch chuẩn của 20 phiên gần nhất, sau đó scale lên năm (252 ngày giao dịch)
            daily_volatility = log_returns.tail(window).std()
            annualized_volatility = daily_volatility * np.sqrt(252)
            
            return float(annualized_volatility * 100) # Trả về phần trăm (%)
        except Exception:
            return None
