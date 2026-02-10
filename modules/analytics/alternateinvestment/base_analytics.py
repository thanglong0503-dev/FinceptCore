"""
Alternative Investments Base Analytics Module
Core financial mathematics and abstract base classes for alternative investment analytics.
Adapted for Fincept Core v1.2
"""

import numpy as np
import pandas as pd
from decimal import Decimal, getcontext, InvalidOperation
from typing import List, Optional, Dict, Any, Tuple, Union
from datetime import datetime
from abc import ABC, abstractmethod
from dataclasses import dataclass
import logging

# --- 1. CẤU TRÚC DỮ LIỆU (DATA MODELS) ---
# Emo thêm phần này để code chạy độc lập không cần file config ngoài

@dataclass
class CashFlow:
    date: str  # Format 'YYYY-MM-DD'
    amount: Decimal
    cf_type: str = 'transaction'  # 'capital_call', 'distribution', 'investment'

@dataclass
class MarketData:
    timestamp: str
    price: Decimal
    volume: Decimal = Decimal('0')

@dataclass
class AssetParameters:
    currency: str
    asset_class: str
    market_region: Optional[str] = None
    management_fee: Optional[Decimal] = None
    performance_fee: Optional[Decimal] = None
    hurdle_rate: Optional[Decimal] = None

class Constants:
    DAYS_IN_YEAR = Decimal('365.25')
    BUSINESS_DAYS_IN_YEAR = Decimal('252')
    MONTHS_IN_YEAR = Decimal('12')

class Config:
    PE_IRR_MAX_ITERATIONS = 100
    PE_IRR_TOLERANCE = 1e-7
    RISK_FREE_RATE = Decimal('0.04')  # 4% risk free

# --- 2. CORE LOGIC (CFA STANDARD) ---

getcontext().prec = 28
logger = logging.getLogger(__name__)

class FinancialMath:
    """Core financial mathematics functions following CFA standards"""

    @staticmethod
    def irr(cash_flows: List[CashFlow], guess: Decimal = Decimal('0.10')) -> Optional[Decimal]:
        """
        Calculate Internal Rate of Return (IRR) using Newton-Raphson method.
        CFA Standard: IRR is the discount rate that makes NPV = 0.
        """
        if not cash_flows:
            return None

        # Sort cash flows by date
        try:
            sorted_cfs = sorted(cash_flows, key=lambda x: x.date)
            dates = [datetime.strptime(cf.date, '%Y-%m-%d') for cf in sorted_cfs]
            amounts = [float(cf.amount) for cf in sorted_cfs]
        except Exception as e:
            logger.error(f"Error processing cash flows: {e}")
            return None

        base_date = dates[0]
        days = [(d - base_date).days for d in dates]

        def npv(rate):
            # Tránh chia cho 0 hoặc số quá nhỏ
            if rate <= -1: return float('inf')
            return sum(amount / (1 + rate) ** (day / 365.25) for amount, day in zip(amounts, days))

        def npv_derivative(rate):
            if rate <= -1: return float('inf')
            return sum(-amount * (day / 365.25) / (1 + rate) ** ((day / 365.25) + 1)
                       for amount, day in zip(amounts, days))

        rate = float(guess)
        for _ in range(Config.PE_IRR_MAX_ITERATIONS):
            try:
                npv_val = npv(rate)
                if abs(npv_val) < float(Config.PE_IRR_TOLERANCE):
                    return Decimal(str(rate))

                npv_deriv = npv_derivative(rate)
                if abs(npv_deriv) < 1e-12:
                    break

                rate = rate - npv_val / npv_deriv
            except (OverflowError, ZeroDivisionError):
                break

        return None

    @staticmethod
    def npv(cash_flows: List[CashFlow], discount_rate: Decimal) -> Decimal:
        """Calculate Net Present Value (NPV). CFA Standard: Σ(CF_t / (1+r)^t)"""
        if not cash_flows:
            return Decimal('0')

        sorted_cfs = sorted(cash_flows, key=lambda x: x.date)
        base_date = datetime.strptime(sorted_cfs[0].date, '%Y-%m-%d')

        npv_value = Decimal('0')
        for cf in sorted_cfs:
            cf_date = datetime.strptime(cf.date, '%Y-%m-%d')
            years = Decimal(str((cf_date - base_date).days)) / Constants.DAYS_IN_YEAR
            present_value = cf.amount / ((Decimal('1') + discount_rate) ** years)
            npv_value += present_value

        return npv_value

    @staticmethod
    def moic(cash_flows: List[CashFlow]) -> Optional[Decimal]:
        """Calculate Multiple of Invested Capital (MOIC). Total Dist / Total Invested."""
        total_invested = Decimal('0')
        total_distributed = Decimal('0')

        for cf in cash_flows:
            if cf.amount < 0:  # Tiền chi ra (Đầu tư)
                total_invested += abs(cf.amount)
            elif cf.amount > 0:  # Tiền thu về (Phân phối)
                total_distributed += cf.amount

        if total_invested == 0:
            return None

        return total_distributed / total_invested

    @staticmethod
    def sharpe_ratio(returns: List[Decimal], risk_free_rate: Decimal = None) -> Decimal:
        """Calculate Sharpe Ratio. (Rp - Rf) / StdDev"""
        if len(returns) < 2:
            return Decimal('0')

        if risk_free_rate is None:
            # Monthly risk free rate default
            risk_free_rate = Config.RISK_FREE_RATE / Constants.MONTHS_IN_YEAR

        excess_returns = [r - risk_free_rate for r in returns]
        mean_excess = sum(excess_returns) / len(excess_returns)

        # Tính Variance (Phương sai)
        variance = sum((r - mean_excess) ** 2 for r in excess_returns) / (len(excess_returns) - 1)
        std_dev = variance.sqrt()

        if std_dev == 0:
            return Decimal('0')

        return mean_excess / std_dev

    @staticmethod
    def maximum_drawdown(prices: List[Decimal]) -> Tuple[Decimal, int, int]:
        """Calculate Maximum Drawdown (Mức sụt giảm sâu nhất từ đỉnh)."""
        if len(prices) < 2:
            return Decimal('0'), 0, 0

        max_dd = Decimal('0')
        peak_idx = 0
        trough_idx = 0
        current_peak = prices[0]
        current_peak_idx = 0

        for i, price in enumerate(prices):
            if price > current_peak:
                current_peak = price
                current_peak_idx = i
            
            # Drawdown luôn là số dương (thể hiện % mất mát)
            drawdown = (current_peak - price) / current_peak
            if drawdown > max_dd:
                max_dd = drawdown
                peak_idx = current_peak_idx
                trough_idx = i

        return max_dd, peak_idx, trough_idx

class AlternativeInvestmentBase(ABC):
    """
    Abstract base class for all alternative investment types.
    Defines common interface and shared functionality.
    """

    def __init__(self, parameters: AssetParameters):
        self.parameters = parameters
        self.market_data: List[MarketData] = []
        self.cash_flows: List[CashFlow] = []
        self.math = FinancialMath()

    def add_market_data(self, data: List[MarketData]) -> None:
        """Add market data history"""
        self.market_data.extend(data)
        self.market_data.sort(key=lambda x: x.timestamp)

    def add_cash_flows(self, cash_flows: List[CashFlow]) -> None:
        """Add investment cash flows"""
        self.cash_flows.extend(cash_flows)
        self.cash_flows.sort(key=lambda x: x.date)

    def get_latest_price(self) -> Optional[Decimal]:
        if not self.market_data:
            return None
        return self.market_data[-1].price

    def calculate_simple_returns(self) -> List[Decimal]:
        """Calculate simple returns from price history"""
        if len(self.market_data) < 2:
            return []
        
        returns = []
        for i in range(1, len(self.market_data)):
            prev = self.market_data[i-1].price
            curr = self.market_data[i].price
            if prev == 0: continue
            ret = (curr - prev) / prev
            returns.append(ret)
        return returns

    def get_performance_summary(self) -> Dict[str, Any]:
        """
        Get comprehensive performance summary (The 'Dashboard' Data)
        """
        returns = self.calculate_simple_returns()
        prices = [md.price for md in self.market_data]

        if not prices:
            return {"error": "No market data available"}

        # Tính toán các chỉ số
        volatility = Decimal('0')
        if returns:
            # Annualized Volatility (Assume Daily Data default)
            base_vol = self.math.sharpe_ratio(returns) # Reusing internal math logic helper if needed
            # Manual volatility calc for simplicity here
            mean_ret = sum(returns) / len(returns)
            var = sum((r - mean_ret)**2 for r in returns) / max(1, len(returns)-1)
            volatility = var.sqrt() * Constants.BUSINESS_DAYS_IN_YEAR.sqrt()

        sharpe = self.math.sharpe_ratio(returns)
        max_dd, _, _ = self.math.maximum_drawdown(prices)
        
        # MOIC calculation if cash flows exist
        moic = self.math.moic(self.cash_flows)

        return {
            'latest_price': float(self.get_latest_price() or 0),
            'volatility_annualized': float(volatility),
            'sharpe_ratio': float(sharpe),
            'max_drawdown': float(max_dd),
            'moic': float(moic) if moic else 0.0,
            'observations': len(prices)
        }

    @abstractmethod
    def calculate_nav(self) -> Decimal:
        pass
