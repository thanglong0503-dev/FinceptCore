# src/backend/macro_data.py
import pandas as pd
from dbnomics import fetch_series
import streamlit as st

class MacroDataEngine:
    """
    Kết nối với DBnomics để lấy dữ liệu kinh tế vĩ mô toàn cầu.
    """
    
    @staticmethod
    @st.cache_data(ttl=86400 * 7)  # Cache 1 tuần vì dữ liệu vĩ mô ít thay đổi
    def fetch_gdp_growth(country_code: str = "USA"):
        """
        Lấy dữ liệu tăng trưởng GDP từ World Bank.
        Mã series cần được tra cứu chính xác từ DBnomics.
        Ví dụ: World Bank WDI (World Development Indicators).
        """
        try:
            # Series ID mẫu cho GDP growth (annual %) của WB
            # Cấu trúc: WB/WDI/NY.GDP.MKTP.KD.ZG-{country_code}
            series_id = f"WB/WDI/NY.GDP.MKTP.KD.ZG-{country_code}"
            df = fetch_series(series_id)
            return df[['period', 'value']].rename(columns={'period': 'Year', 'value': 'GDP Growth'})
        except Exception as e:
            st.warning(f"Không thể lấy dữ liệu GDP cho {country_code}")
            return pd.DataFrame()

    @staticmethod
    @st.cache_data
    def fetch_inflation_rate(country_code: str = "USA"):
        """
        Lấy dữ liệu lạm phát (CPI).
        """
        try:
            # Series ID mẫu cho Inflation, consumer prices (annual %)
            series_id = f"WB/WDI/FP.CPI.TOTL.ZG-{country_code}"
            df = fetch_series(series_id)
            return df[['period', 'value']].rename(columns={'period': 'Year', 'value': 'Inflation Rate'})
        except Exception as e:
            return pd.DataFrame()
