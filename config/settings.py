# File: config/settings.py

class SystemConfig:
    """
    Bộ quản lý cấu hình hệ thống (Tiền tệ, Định dạng số)
    """
    
    # Tỷ giá cố định (Sau này có thể gọi API lấy tỷ giá thực tế ở đây)
    FX_RATES = {
        "USD": 1.0,
        "VND": 25450.0
    }
    
    SYMBOLS = {
        "USD": "$",
        "VND": "₫"
    }

    @staticmethod
    def get_currency_config(currency_code):
        """Trả về cấu hình cho loại tiền tệ được chọn"""
        return {
            "rate": SystemConfig.FX_RATES.get(currency_code, 1.0),
            "symbol": SystemConfig.SYMBOLS.get(currency_code, "$"),
            # VND không dùng số thập phân, USD dùng 2 số
            "format": "{:,.0f}" if currency_code == "VND" else "{:,.2f}"
        }
