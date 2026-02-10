import streamlit as st
import sys
import os
import pandas as pd

# --- SYSTEM SETUP ---
# Thêm đường dẫn để Python tìm thấy các module con
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Cấu hình trang (Luôn phải ở đầu)
st.set_page_config(
    page_title="Fincept Core Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- IMPORT MODULES & CONFIG ---
# 1. Config (Kho Chữ & Kho Số)
try:
    from config.locales import DICTIONARY
    from config.settings import SystemConfig
except ImportError:
    st.error("SYSTEM ERROR: Config files missing. Please check 'config/locales.py' and 'config/settings.py'.")
    st.stop()

# 2. Modules Nghiệp vụ
try:
    from modules.analytics.corporate import DCFValuation
except ImportError: pass

try:
    from modules.analytics.alternateinvestment.asset_location import AssetLocationAnalyzer
except ImportError: pass

# --- SIDEBAR: GIAO DIỆN TỐI GIẢN (MINIMALIST UI) ---
with st.sidebar:
    # Header: Font Monospace, Không Icon
    st.markdown("## FINCEPT CORE")
    st.markdown("`STATUS: ONLINE`")
    st.markdown("---")
    
    # Settings: Gom gọn 1 dòng, ẩn nhãn
    col_lang, col_curr = st.columns(2)
    with col_lang:
        lang_code = st.selectbox("Language", ["VN", "EN"], index=0, label_visibility="collapsed")
    with col_curr:
        curr_code = st.selectbox("Currency", ["VND", "USD"], index=0, label_visibility="collapsed")

    # --- LOAD CẤU HÌNH ---
    # Lấy từ điển ngôn ngữ
    T = DICTIONARY[lang_code]
    
    # Lấy cấu hình tiền tệ
    curr_conf = SystemConfig.get_currency_config(curr_code)
    FX_RATE = curr_conf["rate"]
    SYMBOL = curr_conf["symbol"]
    FMT = curr_conf["format"] # Format số (VD: {:,.0f} cho VND)

    # Hiển thị tỷ giá nhỏ xíu (Tinh tế)
    if curr_code == "VND":
        st.caption(f"FX: 1 USD ≈ {FX_RATE/1000:.1f}k VND")
    else:
        st.caption("FX: Base Currency (USD)")

    st.markdown("---")
    
    # Menu Điều Hướng (Dùng từ điển để dịch tên Menu)
    nav = st.radio(
        "MODULES", 
        [T["nav_dashboard"], T["nav_dcf"], T["nav_cfa"]], 
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    st.caption("v1.2.1 | Production Env")

# --- MAIN CONTENT AREA ---

# ==================================================
# MODULE 1: CORPORATE FINANCE (DCF VALUATION)
# ==================================================
if nav == T["nav_dcf"]:
    st.title(T["dcf_title"])
    st.markdown(f"`{T['dcf_subtitle']}`")
    st.divider()

    col1, col2 = st.columns([1, 2], gap="large")
    
    with col1:
        st.subheader(T["input_header"])
        with st.form("dcf_form"):
            ticker = st.text_input(T["ticker_label"], value="VNM").upper()
            st.markdown("---")
            growth = st.slider(T["growth_label"], 0.0, 0.5, 0.10, 0.01)
            wacc = st.slider(T["wacc_label"], 0.05, 0.20, 0.12, 0.005)
            
            submit_dcf = st.form_submit_button(T["run_btn"])

    with col2:
        st.subheader(T["result_header"])
        if submit_dcf:
            with st.spinner("Processing Financial Data..."):
                try:
                    model = DCFValuation(ticker)
                    # Tính toán gốc (USD)
                    res = model.calculate_dcf(growth, wacc)
                    
                    if res:
                        # --- QUY ĐỔI TIỀN TỆ ---
                        price = res['current_price'] * FX_RATE
                        fair = res['fair_value'] * FX_RATE
                        
                        # --- HIỂN THỊ ---
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.metric(T["metric_price"], f"{SYMBOL}{FMT.format(price)}")
                        with m2:
                            st.metric(T["metric_fair"], f"{SYMBOL}{FMT.format(fair)}")
                        with m3:
                            upside = res['upside']
                            color = "normal" if upside > 0 else "off"
                            st.metric(T["metric_upside"], f"{upside:+.2f}%", delta_color=color)
                            
                        st.divider()
                        
                        # Logic Khuyến Nghị
                        if res['fair_value'] > res['current_price'] * 1.15:
                            st.success(f"**{T['rec_buy']}**")
                        elif res['fair_value'] < res['current_price'] * 0.85:
                            st.error(f"**{T['rec_sell']}**")
                        else:
                            st.warning(f"**{T['rec_hold']}**")
                            
                        # Debug Info
                        with st.expander("Show Raw Data"):
                            st.json(res)
                    else:
                        st.error("Error: Financial data unavailable for this ticker.")
                except Exception as e:
                    st.error(f"System Error: {e}")

# ==================================================
# MODULE 2: ASSET LOCATION (CFA ANALYTICS)
# ==================================================
elif nav == T["nav_cfa"]:
    # Tiêu đề lấy từ Config
    st.title("ASSET LOCATION OPTIMIZATION") 
    st.markdown("`Module: Wealth Management / Tax Efficiency Strategy`")
    st.divider()

    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.subheader(T["input_header"]) # Dùng chung header với DCF
        with st.form("cfa_form"):
            # Asset Class (Giữ tiếng Anh chuyên ngành)
            asset_class = st.selectbox(
                "Asset Class",
                options=[
                    "Stock (Public Equity)",
                    "Index Fund (Passive)",
                    "Bond (Fixed Income)",
                    "REIT (Real Estate)",
                    "Crypto (Long-term Hold)",
                    "Crypto (High-freq Trading)",
                    "Municipal Bond"
                ]
            )
            
            # Số tiền đầu tư
            amount_input = st.number_input(f"Principal Amount ({SYMBOL})", value=10000, step=1000)
            
            # Thời gian & Thuế
            years = st.slider("Time Horizon (Years)", 5, 50, 20)
            tax_rate = st.number_input("Marginal Tax Rate (%)", value=24, min_value=0, max_value=60)
            
            submit_cfa = st.form_submit_button("RUN ANALYSIS")

    with col_right:
        st.subheader("ANALYSIS RESULTS")
        
        if submit_cfa:
            # 1. Chuyển đổi tiền tệ về USD để tính toán (nếu cần) hoặc tính trực tiếp
            # Vì logic Asset Location chỉ nhân chia, ta có thể truyền thẳng số vào
            
            analyzer = AssetLocationAnalyzer(tax_bracket=tax_rate/100)
            result = analyzer.analyze(asset_class, amount_input, years)
            
            # 2. Hiển thị Metrics
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Tax Profile", result['profile'])
            with m2:
                # Format số tiền tiết kiệm được theo tiền tệ đã chọn
                saved_val = result.get('saved_value', 0)
                st.metric("Proj. Tax Alpha", f"{SYMBOL}{FMT.format(saved_val)}")
            with m3:
                # ROI
                roi = (saved_val / amount_input) * 100 if amount_input > 0 else 0
                st.metric("Tax ROI", f"{roi:.2f}%")
            
            st.divider()
            
            # 3. Khuyến nghị chiến lược
            st.markdown("#### STRATEGIC RECOMMENDATION")
            rec = result['recommendation']
            
            if "TAXABLE" in rec or "Thường" in rec:
                st.success(f"**PLACEMENT:** {rec}")
            elif "DEFERRED" in rec or "Hoãn" in rec:
                st.warning(f"**PLACEMENT:** {rec}")
            else:
                st.info(f"**PLACEMENT:** {rec}")
                
            st.markdown(f"> **RATIONALE:** {result['reason']}")

# ==================================================
# MODULE 3: DASHBOARD (PLACEHOLDER)
# ==================================================
elif nav == T["nav_dashboard"]:
    st.title("EXECUTIVE DASHBOARD")
    st.info("Select a module from the sidebar to begin analysis.")
    
    # Một chút giả lập Dashboard
    m1, m2, m3 = st.columns(3)
    m1.metric("S&P 500", "5,420.33", "+1.2%")
    m2.metric("VN-Index", "1,250.45", "-0.5%")
    m3.metric("Bitcoin", "$98,000", "+2.5%")
