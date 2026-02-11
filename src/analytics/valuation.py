import numpy as np

class ValuationEngine:
    @staticmethod
    def calculate_dcf(fcf, growth_rate, terminal_growth, discount_rate, years=5, net_debt=0, shares=1):
        """
        Tính toán DCF đơn giản hóa.
        """
        future_fcf =
        discount_factors =
        
        # Giai đoạn dự phóng
        current = fcf
        for i in range(1, years + 1):
            current *= (1 + growth_rate)
            future_fcf.append(current)
            discount_factors.append((1 + discount_rate) ** i)
            
        pv_stage_1 = sum([f / d for f, d in zip(future_fcf, discount_factors)])
        
        # Giá trị kết dư (Terminal Value)
        # Sử dụng Gordon Growth Model
        terminal_val = (future_fcf[-1] * (1 + terminal_growth)) / (discount_rate - terminal_growth)
        pv_terminal = terminal_val / ((1 + discount_rate) ** years)
        
        enterprise_val = pv_stage_1 + pv_terminal
        equity_val = enterprise_val - net_debt
        fair_value = equity_val / shares if shares > 0 else 0
        
        return {
            "fair_value": fair_value,
            "enterprise_value": enterprise_val,
            "upside": 0.0 # Cần so sánh với giá thị trường bên ngoài
        }
