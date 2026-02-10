# File: config/locales.py

DICTIONARY = {
    "EN": {
        # --- NAVIGATION (MENU) ---
        "nav_dashboard": "00. Dashboard",
        "nav_dcf": "01. Corporate Finance (DCF)",
        "nav_cfa": "02. Asset Location (Tax)",
        "nav_quant": "03. Quantitative Analysis",

        # --- MODULE 01: DCF (Tài chính doanh nghiệp) ---
        "dcf_title": "CORPORATE VALUATION MODEL",
        "dcf_subtitle": "Method: Discounted Cash Flow (DCF) | Source: Yahoo Finance",
        "input_header": "INPUT PARAMETERS",  # <-- Cái Ngài đang bị lỗi thiếu ở đây
        "ticker_label": "Stock Ticker",
        "growth_label": "Growth Rate (5Y)",
        "wacc_label": "Discount Rate (WACC)",
        "run_btn": "RUN VALUATION",
        "result_header": "VALUATION OUTPUT",
        "metric_price": "Current Price",
        "metric_fair": "Fair Value",
        "metric_upside": "Upside / Downside",
        "rec_buy": "RECOMMENDATION: BUY",
        "rec_sell": "RECOMMENDATION: SELL",
        "rec_hold": "RECOMMENDATION: HOLD",

        # --- MODULE 02: CFA (Tối ưu thuế) ---
        # (Module này dùng chung input_header với DCF nên không cần khai báo lại)
        
        # --- MODULE 03: QUANTITATIVE (Phân tích định lượng) ---
        "quant_title": "QUANTITATIVE ANALYSIS LAB",
        "quant_subtitle": "Engine: Fincept Base Analytics | Standard: CFA Level 1 & 2",
        "tab_risk": "Risk Metrics (Sharpe/Drawdown)",
        "tab_project": "Capital Budgeting (IRR/NPV)",
        "input_returns": "Historical Returns Sequence (%)",
        "btn_calc_risk": "CALCULATE RISK METRICS",
        "btn_check_project": "EVALUATE PROJECT"
    },
    "VN": {
        # --- NAVIGATION (MENU) ---
        "nav_dashboard": "00. Bảng Điều Khiển",
        "nav_dcf": "01. Tài Chính Doanh Nghiệp",
        "nav_cfa": "02. Quản Lý Gia Sản (Thuế)",
        "nav_quant": "03. Phân Tích Định Lượng",

        # --- MODULE 01: DCF (Tài chính doanh nghiệp) ---
        "dcf_title": "MÔ HÌNH ĐỊNH GIÁ DCF",
        "dcf_subtitle": "Phương pháp: Chiết khấu dòng tiền | Nguồn: Yahoo Finance",
        "input_header": "THÔNG SỐ ĐẦU VÀO", # <-- Từ khóa quan trọng
        "ticker_label": "Mã Cổ Phiếu (Ticker)",
        "growth_label": "Tốc độ tăng trưởng (5 năm)",
        "wacc_label": "Chi phí vốn (WACC)",
        "run_btn": "CHẠY ĐỊNH GIÁ",
        "result_header": "KẾT QUẢ ĐỊNH GIÁ",
        "metric_price": "Giá thị trường",
        "metric_fair": "Giá trị thực",
        "metric_upside": "Tiềm năng tăng trưởng",
        "rec_buy": "KHUYẾN NGHỊ: MUA (Định giá rẻ)",
        "rec_sell": "KHUYẾN NGHỊ: BÁN (Định giá đắt)",
        "rec_hold": "KHUYẾN NGHỊ: NẮM GIỮ",

        # --- MODULE 02: CFA (Tối ưu thuế) ---
        
        # --- MODULE 03: QUANTITATIVE (Phân tích định lượng) ---
        "quant_title": "PHÒNG LAB ĐỊNH LƯỢNG",
        "quant_subtitle": "Bộ xử lý: Fincept Base Analytics | Tiêu chuẩn: CFA Level 1 & 2",
        "tab_risk": "Đo Lường Rủi Ro (Sharpe/Drawdown)",
        "tab_project": "Thẩm Định Dự Án (IRR/NPV)",
        "input_returns": "Chuỗi Lợi Nhuận Lịch Sử (%)",
        "btn_calc_risk": "TÍNH TOÁN CHỈ SỐ RỦI RO",
        "btn_check_project": "THẨM ĐỊNH DỰ ÁN"
    }
}
