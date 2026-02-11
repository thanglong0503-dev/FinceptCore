"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/analytics/technical.py
ROLE: Quantitative Technical Indicators Engine
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import pandas as pd
import numpy as np

class TechnicalIndicators:
    """Bộ công cụ tính toán các chỉ báo Phân tích Kỹ thuật (TA)"""

    @staticmethod
    def add_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Bơm toàn bộ các chỉ báo kỹ thuật cốt lõi vào bộ dữ liệu OHLCV.
        Bao gồm: Trend (SMA, EMA), Momentum (RSI, MACD), Volatility (Bollinger Bands).
        """
        if df is None or df.empty or 'Close' not in df.columns:
            return df
            
        # Tránh cảnh báo SettingWithCopyWarning của Pandas
        df = df.copy()
        
        try:
            # 1. MOVING AVERAGES (Đường trung bình động)
            # Dùng để xác định xu hướng ngắn/trung/dài hạn
            df['SMA_20'] = df['Close'].rolling(window=20, min_periods=1).mean()
            df['SMA_50'] = df['Close'].rolling(window=50, min_periods=1).mean()
            df['SMA_200'] = df['Close'].rolling(window=200, min_periods=1).mean()
            
            df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
            df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()

            # 2. MACD (Moving Average Convergence Divergence)
            # Đo lường động lượng và xác nhận xu hướng
            df['MACD'] = df['EMA_12'] - df['EMA_26']
            df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
            df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']

            # 3. RSI (Relative Strength Index)
            # Đo lường sức mạnh quá mua (Overbought > 70) / quá bán (Oversold < 30)
            delta = df['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14, min_periods=1).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14, min_periods=1).mean()
            
            # Xử lý lỗi chia cho 0
            rs = np.where(loss == 0, 100, gain / loss)
            df['RSI_14'] = np.where(loss == 0, 100, 100 - (100 / (1 + rs)))

            # 4. BOLLINGER BANDS
            # Đo lường độ biến động và các điểm đảo chiều tiềm năng
            df['BB_Middle'] = df['SMA_20']
            rolling_std = df['Close'].rolling(window=20, min_periods=1).std()
            df['BB_Upper'] = df['BB_Middle'] + (rolling_std * 2)
            df['BB_Lower'] = df['BB_Middle'] - (rolling_std * 2)
            
            # Làm tròn dữ liệu cho gọn gàng
            numeric_cols = df.select_dtypes(include=['float64', 'float32']).columns
            df[numeric_cols] = df[numeric_cols].round(4)
            
            return df
        except Exception as e:
            print(f"Technical Analysis Error: {e}")
            return df # Trả về DF gốc nếu lỗi
