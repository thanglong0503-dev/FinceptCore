# Snippet logic tính toán VaR trong Python
import numpy as np
from scipy.stats import norm

def calculate_var(returns, confidence_level=0.95):
    """
    Tính VaR theo 2 phương pháp: Tham số (Parametric) và Lịch sử (Historical).
    """
    # 1. Historical VaR
    var_historical = np.percentile(returns, (1 - confidence_level) * 100)
    
    # 2. Parametric VaR (giả định phân phối chuẩn)
    mu = np.mean(returns)
    sigma = np.std(returns)
    var_parametric = norm.ppf(1 - confidence_level, mu, sigma)
    
    # 3. Conditional VaR (Expected Shortfall)
    # Trung bình của các khoản lỗ vượt quá VaR
    cvar = returns[returns <= var_historical].mean()
    
    return var_historical, var_parametric, cvar
