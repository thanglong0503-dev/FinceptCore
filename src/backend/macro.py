"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/backend/macro.py
ROLE: Macroeconomic Data Engine (Kéo dữ liệu vĩ mô, lãi suất)
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import yfinance as yf
import streamlit as st
import logging
from typing import Optional

logger = logging.getLogger(__name__)

class MacroEngine:
    """Động cơ xử lý dữ liệu Vĩ mô (Lãi suất, Lạm phát, GDP)"""

    @staticmethod
    @st.cache_data(ttl=86400, show_spinner=False) # Lãi suất ít biến động, cache 1 ngày (86400s)
    def get_risk_free_rate() -> float:
        """
        Lấy lợi suất Trái phiếu Chính phủ Mỹ 10 năm (^TNX) làm Risk-Free Rate.
        Trả về dưới dạng số thập phân (VD: 4.2% -> 0.042)
        """
        logger.info("FETCHING MACRO: US 10-Year Treasury Yield (^TNX)")
        try:
            # Lấy mã ^TNX từ Yahoo Finance
            tnx = yf.Ticker("^TNX")
            df = tnx.history(period="5d")
            
            if df is not None and not df.empty:
                # Lấy giá đóng cửa phiên gần nhất, chia 100 vì ^TNX hiển thị dạng % (VD: 4.2)
                yield_pct = float(df['Close'].iloc[-1])
                return yield_pct / 100.0
            else:
                raise ValueError("No data returned for ^TNX")
                
        except Exception as e:
            logger.warning(f"Macro Engine Warning: Không lấy được ^TNX ({e}). Dùng fallback 4.25%")
            return 0.0425 # Fallback an toàn (4.25%) nếu API lỗi
