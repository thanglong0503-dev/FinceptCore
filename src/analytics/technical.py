import pandas_ta as ta
import pandas as pd

class TechnicalEngine:
    @staticmethod
    def calculate_core_indicators(df: pd.DataFrame):
        if df.empty: return df
        data = df.copy()
        
        # Trend
        data.ta.sma(length=50, append=True)
        data.ta.sma(length=200, append=True)
        data.ta.ema(length=21, append=True)
        
        # Momentum
        data.ta.rsi(length=14, append=True)
        data.ta.macd(fast=12, slow=26, signal=9, append=True)
        
        # Volatility
        data.ta.bbands(length=20, std=2, append=True)
        data.ta.atr(length=14, append=True)
        
        return data
