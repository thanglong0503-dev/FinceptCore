import yfinance as yf
import pandas as pd
import streamlit as st

class MarketEngine:
    @staticmethod
    @st.cache_data(ttl=60)
    def get_realtime_price(ticker):
        try:
            t = yf.Ticker(ticker)
            # Sử dụng fast_info để tối ưu tốc độ
            price = t.fast_info.last_price
            prev_close = t.fast_info.previous_close
            change = ((price - prev_close) / prev_close) * 100
            return {
                "symbol": ticker,
                "price": round(price, 2),
                "change": round(change, 2),
                "volume": t.fast_info.last_volume
            }
        except Exception:
            return {"symbol": ticker, "price": 0.0, "change": 0.0, "volume": 0}

    @staticmethod
    @st.cache_data(ttl=3600)
    def get_historical_data(ticker, period="1y", interval="1d"):
        try:
            df = yf.download(ticker, period=period, interval=interval, progress=False)
            if df.empty: return pd.DataFrame()
            # Xử lý MultiIndex nếu có (yfinance v0.2+)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            return df
        except:
            return pd.DataFrame()

    @staticmethod
    @st.cache_data(ttl=86400)
    def get_fundamentals(ticker):
        try:
            t = yf.Ticker(ticker)
            return {
                "info": t.info,
                "financials": t.financials,
                "balance_sheet": t.balance_sheet,
                "cashflow": t.cashflow
            }
        except:
            return None
