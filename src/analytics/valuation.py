# src/analytics/fundamental.py
import numpy as np

class FundamentalAnalyzer:
    @staticmethod
    def dcf_valuation(
        current_fcf: float,
        growth_rate_5y: float,
        terminal_growth_rate: float,
        discount_rate: float,
        net_debt: float,
        shares_outstanding: float
    ):
        """
        Tính toán giá trị nội tại (Intrinsic Value) của cổ phiếu theo phương pháp DCF 2 giai đoạn.
        
        Args:
            current_fcf: Dòng tiền tự do hiện tại (TTM).
            growth_rate_5y: Tốc độ tăng trưởng dự kiến trong 5 năm tới (ví dụ: 0.10 cho 10%).
            terminal_growth_rate: Tốc độ tăng trưởng dài hạn (ví dụ: 0.025).
            discount_rate: Chi phí vốn bình quân gia quyền (WACC) (ví dụ: 0.09).
            net_debt: Nợ ròng (Tổng nợ - Tiền mặt).
            shares_outstanding: Số lượng cổ phiếu đang lưu hành.
            
        Returns:
            dict: Kết quả định giá chi tiết.
        """
        future_cash_flows =
        discount_factors =
        
        # Giai đoạn 1: Tăng trưởng nhanh (5 năm)
        fcf = current_fcf
        for i in range(1, 6):
            fcf = fcf * (1 + growth_rate_5y)
            future_cash_flows.append(fcf)
            discount_factors.append((1 + discount_rate) ** i)
            
        # Tính hiện giá của dòng tiền giai đoạn 1
        pv_stage_1 = sum([fcf / df for fcf, df in zip(future_cash_flows, discount_factors)])
        
        # Giai đoạn 2: Giá trị kết dư (Terminal Value)
        last_fcf = future_cash_flows[-1]
        terminal_value = (last_fcf * (1 + terminal_growth_rate)) / (discount_rate - terminal_growth_rate)
        
        # Hiện giá của Terminal Value
        pv_terminal_value = terminal_value / ((1 + discount_rate) ** 5)
        
        # Giá trị doanh nghiệp (Enterprise Value)
        enterprise_value = pv_stage_1 + pv_terminal_value
        
        # Giá trị vốn chủ sở hữu (Equity Value)
        equity_value = enterprise_value - net_debt
        
        # Giá trị mỗi cổ phiếu
        fair_value = equity_value / shares_outstanding
        
        return {
            "fair_value": fair_value,
            "enterprise_value": enterprise_value,
            "pv_stage_1": pv_stage_1,
            "pv_terminal": pv_terminal_value
        }
