import streamlit as st
import sys
import os

# --- SYSTEM SETUP ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))
st.set_page_config(page_title="Fincept Core Global", layout="wide", initial_sidebar_state="expanded")

# --- IMPORT MODULES & CONFIG (MỚI) ---
from config.locales import DICTIONARY       # <-- Import Kho Chữ
from config.settings import SystemConfig    # <-- Import Kho Số

# Import logic nghiệp vụ
try:
    from modules.analytics.corporate import DCFValuation
except ImportError: pass

# --- SIDEBAR: CẤU HÌNH TOÀN CẦU ---
with st.sidebar:
    st.markdown("### 🦅 FINCEPT CORE")
    st.caption("🌐 GLOBAL SETTINGS")
    
    col1, col2 = st.columns(2)
    with col1:
        lang_code = st.selectbox("Language", ["VN", "EN"])
    with col2:
        curr_code = st.selectbox("Currency", ["VND", "USD"])

    # 1. LẤY TỪ ĐIỂN
    T = DICTIONARY[lang_code]

    # 2. LẤY CẤU HÌNH TIỀN TỆ
    curr_conf = SystemConfig.get_currency_config(curr_code)
    FX_RATE = curr_conf["rate"]
    SYMBOL = curr_conf["symbol"]
    FMT = curr_conf["format"]

    st.markdown("---")
    
    # Menu dùng từ điển để hiển thị
    nav = st.radio("MODULES", 
                   [T["nav_dashboard"], T["nav_dcf"], T["nav_cfa"]], 
                   label_visibility="collapsed")
    
    # Hiển thị tỷ giá
    st.info(T["currency_note"].format(rate=f"{SystemConfig.FX_RATES['VND']:,.0f}"))

# --- MAIN CONTENT ---

# === MODULE: DCF VALUATION ===
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
            growth = st.slider(T["growth_label"], 0.0, 0.5, 0.10)
            wacc = st.slider(T["wacc_label"], 0.05, 0.20, 0.12)
            submit = st.form_submit_button(T["run_btn"])

    with col2:
        st.subheader(T["result_header"])
        if submit:
            with st.spinner("Processing..."):
                try:
                    model = DCFValuation(ticker)
                    # Tính toán bằng USD (Gốc)
                    res = model.calculate_dcf(growth, wacc)
                    
                    if res:
                        # QUY ĐỔI TIỀN TỆ (Sử dụng config)
                        price = res['current_price'] * FX_RATE
                        fair = res['fair_value'] * FX_RATE
                        
                        m1, m2, m3 = st.columns(3)
                        with m1:
                            st.metric(T["metric_price"], f"{SYMBOL}{FMT.format(price)}")
                        with m2:
                            st.metric(T["metric_fair"], f"{SYMBOL}{FMT.format(fair)}")
                        with m3:
                            # Upside là % nên không cần đổi tiền
                            upside = res['upside']
                            color = "normal" if upside > 0 else "off"
                            st.metric(T["metric_upside"], f"{upside:+.2f}%", delta_color=color)
                            
                        st.divider()
                        
                        # Logic khuyến nghị
                        if res['fair_value'] > res['current_price'] * 1.15:
                            st.success(f"**{T['rec_buy']}**")
                        elif res['fair_value'] < res['current_price'] * 0.85:
                            st.error(f"**{T['rec_sell']}**")
                        else:
                            st.warning(f"**{T['rec_hold']}**")
                            
                except Exception as e:
                    st.error(f"Error: {e}")

# === CÁC MODULE KHÁC ===
elif nav == T["nav_dashboard"]:
    st.title("DASHBOARD")
    st.info("Select a module to start.")
elif nav == T["nav_cfa"]:
    st.title("CFA ANALYTICS")
    st.info("Coming soon...")
