import streamlit as st
import sys
import os
import pandas as pd

# --- SYSTEM CONFIGURATION ---
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Page Setup: Wide layout, professional title
st.set_page_config(
    page_title="Fincept Core Terminal",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- CSS INJECTION (TẠO GIAO DIỆN CHUYÊN NGHIỆP) ---
# Ép font chữ Monospace cho tiêu đề và Sans-serif cho nội dung
st.markdown("""
    <style>
        /* Chỉnh font toàn bộ ứng dụng */
        .stApp {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
        }
        /* Tiêu đề mang phong cách Terminal */
        h1, h2, h3 {
            font-family: 'Roboto Mono', 'Courier New', monospace;
            font-weight: 600;
            letter-spacing: -0.5px;
        }
        /* Loại bỏ padding thừa của Streamlit */
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        /* Style cho Sidebar */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa; /* Màu xám nhẹ công nghiệp */
        }
        /* Style cho Metric Value */
        div[data-testid="stMetricValue"] {
            font-family: 'Roboto Mono', monospace;
            font-size: 1.8rem;
        }
    </style>
""", unsafe_allow_html=True)

# --- MODULE IMPORT ---
try:
    from modules.analytics.alternateinvestment.asset_location import AssetLocationAnalyzer
except ImportError:
    st.error("SYSTEM ERROR: Module 'asset_location' not found. Please verify directory structure.")
    st.stop()

# --- SIDEBAR NAVIGATION ---
with st.sidebar:
    st.markdown("### FINCEPT CORE")
    st.markdown("`v1.0.2-stable`")
    st.markdown("---")
    
    # Menu dạng danh sách đơn giản
    nav_selection = st.radio(
        "MODULE SELECTION",
        ["Dashboard", "CFA Analytics", "Whale Tracking", "System Logs"],
        label_visibility="collapsed" # Ẩn nhãn để tối giản
    )
    
    st.markdown("---")
    st.markdown("**SESSION INFO**")
    st.text(f"User: Admin")
    st.text(f"Status: Connected")
    st.text(f"Env: Production")

# --- MAIN CONTENT AREA ---

# === MODULE: CFA ANALYTICS ===
if nav_selection == "CFA Analytics":
    # Header khu vực
    st.title("ASSET LOCATION OPTIMIZATION")
    st.markdown("`Module: Wealth Management / Tax Efficiency Strategy`")
    st.markdown("---")

    # Layout: 1/3 Input (Trái) - 2/3 Output (Phải)
    col_left, col_right = st.columns([1, 2], gap="large")

    with col_left:
        st.subheader("INPUT PARAMETERS")
        with st.form("analysis_form"):
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
            
            investment_amount = st.number_input("Principal Amount ($)", value=10000, step=1000, format="%d")
            
            time_horizon = st.slider("Time Horizon (Years)", 5, 50, 20)
            
            marginal_tax_rate = st.number_input("Marginal Tax Rate (%)", value=24, min_value=0, max_value=60)
            
            st.markdown("<br>", unsafe_allow_html=True)
            submit_btn = st.form_submit_button("RUN ANALYSIS")

    with col_right:
        st.subheader("ANALYSIS RESULTS")
        
        if submit_btn:
            # Xử lý logic
            analyzer = AssetLocationAnalyzer(tax_bracket=marginal_tax_rate/100)
            result = analyzer.analyze(asset_class, investment_amount, time_horizon)
            
            # 1. Key Metrics Row
            m1, m2, m3 = st.columns(3)
            with m1:
                st.metric("Tax Efficiency Profile", result['profile'])
            with m2:
                saved_val = result.get('saved_value', 0)
                st.metric("Projected Tax Alpha", f"${saved_val:,.2f}", help="Estimated value saved by optimal placement")
            with m3:
                # Tính ROI đơn giản từ việc tiết kiệm thuế
                roi = (saved_val / investment_amount) * 100 if investment_amount > 0 else 0
                st.metric("Tax ROI", f"{roi:.2f}%")
            
            st.divider()
            
            # 2. Strategic Recommendation
            st.markdown("#### STRATEGIC RECOMMENDATION")
            
            # Logic hiển thị thông báo nghiệp vụ (Business Logic Display)
            rec_text = result['recommendation']
            reason_text = result['reason']
            
            # Sử dụng các box thông báo chuẩn UI
            if "TAXABLE" in rec_text or "Thường" in rec_text:
                st.success(f"**PLACEMENT:** {rec_text}")
            elif "DEFERRED" in rec_text or "Hoãn" in rec_text:
                st.warning(f"**PLACEMENT:** {rec_text}")
            else:
                st.info(f"**PLACEMENT:** {rec_text}")
                
            st.markdown(f"> **RATIONALE:** {reason_text}")
            
            # 3. Data Table (Bảng dữ liệu)
            st.markdown("#### DATA BREAKDOWN")
            df_data = pd.DataFrame({
                "Metric": ["Initial Principal", "Horizon", "Tax Bracket", "Est. Tax Drag"],
                "Value": [f"${investment_amount:,.0f}", f"{time_horizon} Years", f"{marginal_tax_rate}%", "Variable"]
            })
            st.dataframe(df_data, use_container_width=True, hide_index=True)

        else:
            # Màn hình chờ (Idle State)
            st.info("System Ready. Awaiting Input Parameters...")
            st.markdown("##### Reference Table: Tax Efficiency Scored")
            
            # Bảng tham chiếu tĩnh
            ref_data = pd.DataFrame({
                "Asset Class": ["REITs / Active Crypto", "Corporate Bonds", "Stocks / ETFs", "Muni Bonds"],
                "Tax Drag": ["High (Inefficient)", "Medium", "Low (Efficient)", "None"],
                "Optimal Account": ["Tax-Deferred (IRA/401k)", "Tax-Deferred", "Taxable Brokerage", "Taxable Brokerage"]
            })
            st.dataframe(ref_data, use_container_width=True, hide_index=True)

# === MODULE: WHALE TRACKING ===
elif nav_selection == "Whale Tracking":
    st.title("WHALE WALLET TRACKING")
    st.markdown("`Module: On-chain Analytics / High Net Worth Individuals`")
    st.markdown("---")
    st.warning("Status: MAINTENANCE_MODE. Module is currently offline for upgrades.")

# === MODULE: DASHBOARD ===
elif nav_selection == "Dashboard":
    st.title("EXECUTIVE DASHBOARD")
    st.markdown("---")
    st.info("Select a specific module from the sidebar to begin analysis.")
