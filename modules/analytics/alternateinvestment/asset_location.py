from decimal import Decimal, getcontext
from enum import Enum

# Cấu hình độ chính xác tiền tệ
getcontext().prec = 28

# Định nghĩa các Enum (Giống code gốc nhưng gọn hơn)
class AccountType(Enum):
    TAXABLE = "Taxable Brokerage (Tài khoản Thường)"
    TAX_DEFERRED = "Tax-Deferred (IRA/401k - Hoãn thuế)"
    TAX_FREE = "Tax-Free (Roth - Miễn thuế)"

class AssetTaxProfile(Enum):
    VERY_TAX_EFFICIENT = "Very Efficient (Rất Hiệu quả)"
    TAX_EFFICIENT = "Efficient (Hiệu quả)"
    TAX_NEUTRAL = "Neutral (Trung tính)"
    TAX_INEFFICIENT = "Inefficient (Kém hiệu quả)"
    VERY_TAX_INEFFICIENT = "Very Inefficient (Rất kém - Né gấp)"

class AssetLocationAnalyzer:
    """
    Asset Location Logic - Adapted for Fincept Core
    """
    
    def __init__(self, tax_bracket=0.24):
        self.tax_bracket = Decimal(str(tax_bracket))

    def _get_tax_profile(self, asset_class):
        """Map asset class to tax efficiency profile"""
        # Chuẩn hóa tên đầu vào
        ac = asset_class.lower()
        
        mapping = {
            'municipal bond': AssetTaxProfile.VERY_TAX_EFFICIENT,
            'crypto (hold)': AssetTaxProfile.VERY_TAX_EFFICIENT, # Long-term crypto gains are cap gains
            'stock (public equity)': AssetTaxProfile.TAX_EFFICIENT,
            'index fund (passive)': AssetTaxProfile.TAX_EFFICIENT,
            'index fund': AssetTaxProfile.TAX_EFFICIENT,
            'stock': AssetTaxProfile.TAX_EFFICIENT,
            
            'bond (fixed income)': AssetTaxProfile.TAX_INEFFICIENT,
            'bond': AssetTaxProfile.TAX_INEFFICIENT,
            'corporate bonds': AssetTaxProfile.TAX_INEFFICIENT,
            
            'reit (real estate)': AssetTaxProfile.VERY_TAX_INEFFICIENT,
            'reit': AssetTaxProfile.VERY_TAX_INEFFICIENT,
            'crypto (high-freq trading)': AssetTaxProfile.VERY_TAX_INEFFICIENT,
            'active crypto': AssetTaxProfile.VERY_TAX_INEFFICIENT
        }
        # Mặc định trả về Trung Tính
        return mapping.get(ac, AssetTaxProfile.TAX_NEUTRAL)

    def analyze(self, asset_class, amount, years=20):
        """
        Hàm chính mà main.py đang gọi.
        Nó sẽ thực hiện tính toán và trả về kết quả chuẩn format.
        """
        profile = self._get_tax_profile(asset_class)
        amount = Decimal(str(amount))
        annual_return = Decimal('0.08') # Giả định lợi nhuận 8%/năm
        
        # 1. Logic Khuyến Nghị (Strategic Recommendation)
        rec = ""
        reason = ""
        
        if profile in [AssetTaxProfile.VERY_TAX_INEFFICIENT, AssetTaxProfile.TAX_INEFFICIENT]:
            rec = AccountType.TAX_DEFERRED.value
            reason = "Tài sản này tạo ra thu nhập chịu thuế cao (lãi suất/cổ tức). Đặt vào ví Hoãn thuế để tránh bị đánh thuế thu nhập cá nhân hàng năm."
        elif profile in [AssetTaxProfile.VERY_TAX_EFFICIENT, AssetTaxProfile.TAX_EFFICIENT]:
            rec = AccountType.TAXABLE.value
            reason = "Tài sản này vốn đã hiệu quả về thuế (Capital Gains thấp). Đặt vào ví Thường để dành không gian quý giá trong ví Hưu trí cho các tài sản khác."
        else:
            rec = "Flexible (Linh hoạt)"
            reason = "Hiệu quả thuế ở mức trung bình. Có thể cân nhắc tùy vào thanh khoản."

        # 2. Tính toán Lợi ích (Value Added)
        # Tax Drag: Mức giảm lợi nhuận do thuế
        if "INEFFICIENT" in profile.name:
            tax_drag = Decimal('0.025') # Mất 2.5% mỗi năm nếu để sai chỗ
        elif "NEUTRAL" in profile.name:
            tax_drag = Decimal('0.01')
        else:
            tax_drag = Decimal('0.00')

        # Giá trị tương lai nếu để đúng chỗ (Lãi kép 8%)
        fv_optimal = amount * ((1 + annual_return) ** years)
        
        # Giá trị tương lai nếu để sai chỗ (Lãi kép bị trừ thuế hàng năm)
        fv_suboptimal = amount * ((1 + annual_return - tax_drag) ** years)
        
        # Tiền tiết kiệm được
        saved_value = float(fv_optimal - fv_suboptimal)

        return {
            "profile": profile.value,
            "recommendation": rec,
            "reason": reason,
            "saved_value": saved_value
        }
