"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/analytics/valuation.py
ROLE: Corporate Valuation Models (DCF, Multiples)
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import pandas as pd
from decimal import Decimal
import logging
from typing import Dict, Any

from src.backend.market import MarketDataEngine
from src.backend.macro import MacroEngine

logger = logging.getLogger(__name__)

class DCFValuation:
    """Mô hình Định giá Chiết khấu Dòng tiền (Discounted Cash Flow) tự động"""

    def __init__(self, ticker: str):
        self.ticker = ticker.upper()
        # Tự động nạp dữ liệu từ các Node khác
        self.info = MarketDataEngine.get_company_info(ticker)
        self.financials = MarketDataEngine.get_financial_statements(ticker)
        self.risk_free_rate = MacroEngine.get_risk_free_rate()

    def _extract_fcf(self) -> float:
        """Thuật toán nội bộ: Trích xuất Dòng tiền tự do (FCF) từ BCTC"""
        cf_stmt = self.financials.get('cash_flow')
        if cf_stmt is None or cf_stmt.empty:
            return 0.0
            
        try:
            # Thử các tên biến phổ biến trong Yahoo Finance
            ocf = 0.0
            if 'Operating Cash Flow' in cf_stmt.index:
                ocf = cf_stmt.loc['Operating Cash Flow'].iloc[0]
            elif 'Total Cash From Operating Activities' in cf_stmt.index:
                ocf = cf_stmt.loc['Total Cash From Operating Activities'].iloc[0]
                
            capex = 0.0
            if 'Capital Expenditure' in cf_stmt.index:
                capex = cf_stmt.loc['Capital Expenditure'].iloc[0]
                
            # FCF = OCF + CapEx (CapEx thường ghi số âm nên dùng dấu cộng)
            fcf = float(ocf + capex)
            
            # Fallback nếu tính ra 0 hoặc lỗi, cố gắng lấy từ 'info'
            if fcf == 0.0 and self.info.get('freeCashflow'):
                fcf = float(self.info.get('freeCashflow'))
                
            return fcf
        except Exception as e:
            logger.error(f"Error extracting FCF for {self.ticker}: {e}")
            return float(self.info.get('freeCashflow', 0.0))

    def calculate(self, growth_rate_1_5: float, terminal_growth: float, equity_risk_premium: float) -> Dict[str, Any]:
        """
        Thực thi mô hình DCF 2 giai đoạn (5 năm tăng trưởng + Vĩnh viễn).
        """
        if "error" in self.info:
            return {"error": self.info["error"]}

        try:
            # 1. Thu thập dữ liệu gốc
            fcf_base = self._extract_fcf()
            if fcf_base <= 0:
                return {"error": "Dòng tiền tự do (FCF) âm hoặc không có dữ liệu. Không thể dùng DCF."}

            total_debt = float(self.info.get('totalDebt', 0.0))
            total_cash = float(self.info.get('totalCash', 0.0))
            shares_out = float(self.info.get('sharesOutstanding', 0.0))
            beta = float(self.info.get('beta', 1.0))
            current_price = float(self.info.get('current_price', 0.0))

            if shares_out == 0 or current_price == 0:
                return {"error": "Thiếu dữ liệu Số lượng cổ phiếu hoặc Giá hiện tại."}

            # 2. Tính toán Chi phí Vốn (WACC - Ở đây đơn giản hóa bằng Cost of Equity CAPM)
            # Ke = Rf + Beta * ERP
            cost_of_equity = self.risk_free_rate + (beta * equity_risk_premium)
            wacc = cost_of_equity # Giả định WACC ~ Ke (Phù hợp cho định giá nhanh)
            
            # Bảo vệ lỗi chia cho 0 hoặc WACC quá nhỏ
            wacc = max(wacc, terminal_growth + 0.01) 

            # 3. Phóng chiếu Dòng tiền 5 năm tới (Giai đoạn 1)
            projected_fcfs = []
            pv_fcfs = 0.0
            current_fcf = fcf_base
            
            for year in range(1, 6):
                current_fcf *= (1 + growth_rate_1_5)
                projected_fcfs.append(current_fcf)
                # Chiết khấu về hiện tại
                pv_fcfs += current_fcf / ((1 + wacc) ** year)

            # 4. Tính Giá trị vĩnh viễn (Terminal Value - Giai đoạn 2)
            # Công thức Gordon Growth: TV = FCF_5 * (1 + g) / (WACC - g)
            terminal_value = (projected_fcfs[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
            pv_tv = terminal_value / ((1 + wacc) ** 5)

            # 5. Tổng hợp Giá trị Doanh nghiệp (Enterprise Value) & Vốn hóa (Equity Value)
            enterprise_value = pv_fcfs + pv_tv
            equity_value = enterprise_value + total_cash - total_debt
            
            # 6. Giá trị nội tại mỗi cổ phiếu (Fair Value per Share)
            fair_value = equity_value / shares_out
            
            # Tính Upside / Downside
            upside_pct = ((fair_value - current_price) / current_price) * 100

            return {
                "ticker": self.ticker,
                "current_price": current_price,
                "fair_value": fair_value,
                "upside_pct": upside_pct,
                "fcf_base": fcf_base,
                "wacc": wacc,
                "enterprise_value": enterprise_value,
                "equity_value": equity_value,
                "currency": self.info.get('currency', 'USD'),
                "assumptions": {
                    "rf": self.risk_free_rate,
                    "beta": beta,
                    "erp": equity_risk_premium,
                    "growth": growth_rate_1_5,
                    "terminal_g": terminal_growth
                }
            }
        except Exception as e:
            return {"error": f"Lỗi tính toán hệ thống: {str(e)}"}
