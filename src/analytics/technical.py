
# src/analytics/technical.py
import pandas_ta as ta
import pandas as pd

class TechnicalAnalyzer:
    """
    Thực hiện tính toán các chỉ báo kỹ thuật trên DataFrame.
    """
    
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> pd.DataFrame:
        """
        Bổ sung các cột chỉ báo kỹ thuật vào DataFrame gốc.
        """
        if df.empty: return df
        
        data = df.copy()
        
        # 1. Trend Indicators (Chỉ báo xu hướng)
        # SMA: Simple Moving Average
        data = ta.sma(data['Close'], length=50)
        data = ta.sma(data['Close'], length=200)
        
        # EMA: Exponential Moving Average
        data['EMA_12'] = ta.ema(data['Close'], length=12)
        data['EMA_26'] = ta.ema(data['Close'], length=26)
        
        # 2. Momentum Indicators (Chỉ báo động lượng)
        # RSI: Relative Strength Index
        data = ta.rsi(data['Close'], length=14)
        
        # MACD: Moving Average Convergence Divergence
        macd = ta.macd(data['Close'])
        # macd trả về 3 cột: MACD_12_26_9, MACDh_12_26_9 (Histogram), MACDs_12_26_9 (Signal)
        data = pd.concat([data, macd], axis=1)
        
        # 3. Volatility Indicators (Chỉ báo biến động)
        # Bollinger Bands
        bbands = ta.bbands(data['Close'], length=20, std=2)
        data = pd.concat([data, bbands], axis=1)
        
        return data

    @staticmethod
    def generate_signals(df: pd.DataFrame):
        """
        Tạo tín hiệu mua/bán dựa trên các quy tắc kỹ thuật đơn giản.
        """
        signals =
        if df.empty or len(df) < 200: return signals
        
        last_row = df.iloc[-1]
        prev_row = df.iloc[-2]
        
        # Golden Cross: SMA 50 cắt lên trên SMA 200
        if prev_row < prev_row and last_row > last_row:
            signals.append({"type": "BULLISH", "signal": "Golden Cross", "desc": "SMA 50 vừa cắt lên trên SMA 200"})
            
        # RSI Oversold: RSI < 30
        if last_row < 30:
            signals.append({"type": "BULLISH", "signal": "RSI Oversold", "desc": f"RSI đang ở mức {last_row:.2f}, thị trường có thể bị bán quá mức"})
            
        return signals
