# src/ai/tools.py
from langchain.tools import tool
from src.backend.market_data import MarketDataEngine
from src.analytics.technical import TechnicalAnalyzer

class FinancialTools:
    
    @tool("get_stock_price")
    def get_stock_price(ticker: str):
        """
        Hữu ích khi cần biết giá hiện tại của một mã cổ phiếu. 
        Đầu vào là mã chứng khoán (ví dụ: AAPL, TSLA).
        """
        data = MarketDataEngine.fetch_real_time_quote(ticker)
        if data:
            return f"Giá hiện tại của {ticker} là {data['price']} {data['currency']}, thay đổi {data['pct_change']:.2f}%."
        return "Không tìm thấy dữ liệu."

    @tool("technical_analysis_summary")
    def technical_analysis_summary(ticker: str):
        """
        Hữu ích khi cần phân tích kỹ thuật, xem xét chỉ báo RSI, MACD để biết xu hướng mua hay bán.
        """
        df = MarketDataEngine.fetch_historical_ohlcv(ticker, period="6mo")
        if df.empty: return "Không có dữ liệu lịch sử."
        
        df_analyzed = TechnicalAnalyzer.calculate_indicators(df)
        last_row = df_analyzed.iloc[-1]
        
        summary = (
            f"Phân tích kỹ thuật cho {ticker}:\n"
            f"- RSI (14): {last_row:.2f}\n"
            f"- Giá đóng cửa: {last_row['Close']}\n"
            f"- SMA 50: {last_row:.2f}, SMA 200: {last_row:.2f}\n"
        )
        
        if last_row > 70: summary += " -> Cảnh báo: Vùng quá mua (Overbought).\n"
        elif last_row < 30: summary += " -> Cảnh báo: Vùng quá bán (Oversold).\n"
            
        return summary
