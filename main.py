import streamlit as st
import sys
import os

# --- 1. CẤU HÌNH HỆ THỐNG ---
# Thêm đường dẫn gốc để Python tìm thấy các module con
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

# Cấu hình trang Streamlit (Phải để đầu tiên)
st.set_page_config(
    page_title="Fincept Core",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 2. IMPORT MODULE ---
# (Đường dẫn mới: analytics -> alternateinvestment -> asset_location)
try:
    from modules.analytics.alternateinvestment.asset_location import AssetLocationAnalyzer
except ImportError as e:
    st.error(f"⚠️ LỖI CẤU TRÚC: Không tìm thấy file code.")
    st.warning("Gợi ý: Ngài hãy kiểm tra xem đã có file '__init__.py' trong thư mục 'alternateinvestment' chưa?")
    st.stop()

# --- 3. GIAO DIỆN SIDEBAR (MENU) ---
with st.sidebar:
    st.title("🦅 FINCEPT CORE")
    st.caption("Enterprise Financial Intelligence")
    st.markdown("---")
    
    # Menu điều hướng
    menu = st.radio(
        "🎯 TRUNG TÂM ĐIỀU KHIỂN:",
        ["📊 CFA Analytics (Thuế)", "🐋 Whale Hunter (Sắp ra mắt)", "⚙️ Cài Đặt"]
    )
    
    st.markdown("---")
    st.info("System Status: 🟢 Online")
    st.caption("v1.0.2 | Built with Python 🐍")

# --- 4. KHU VỰC CHÍNH (MAIN CONTENT) ---

# === TAB 1: CFA ANALYTICS (ASSET LOCATION) ===
if menu == "📊 CFA Analytics (Thuế)":
    st.header("🧠 Tối Ưu Hóa Vị Trí Tài Sản (Asset Location)")
    st.markdown("""
    > *"Đừng để lợi nhuận của Ngài bị Thuế bào mòn. Hãy đặt tài sản đúng chỗ!"* > (Dựa trên giáo trình **CFA Level 3** - Quản lý gia sản).
    """)
    st.markdown("---")

    # Chia cột: Bên trái nhập liệu, Bên phải hiện kết quả
    col_input, col_result = st.columns([1, 2])
    
    with col_input:
        st.subheader("📝 Nhập Thông Tin")
        with st.form("cfa_form"):
            # Chọn loại tài sản
            asset_type = st.selectbox("1. Loại Tài Sản Đầu Tư:", 
                [
                    "Stock (Cổ phiếu thường)", 
                    "Index Fund (Quỹ chỉ số)", 
                    "Bond (Trái phiếu)", 
                    "REIT (Bất động sản)", 
                    "Crypto (Hold dài hạn)", 
                    "Crypto (Trade lướt sóng)", 
                    "Municipal Bond (TP Đô thị)"
                ]
            )
            
            # Nhập số tiền
            amount = st.number_input("2. Số Tiền Dự Kiến ($):", value=10000, step=1000)
            
            # Chọn thời gian & Thuế
            years = st.slider("3. Thời gian nắm giữ (Năm):", 5, 40, 20)
            tax_rate = st.slider("4. Thuế suất thu nhập (%):", 0, 50, 24)
            
            # Nút bấm hành động
            submit_btn = st.form_submit_button("🚀 PHÂN TÍCH NGAY")
            
    with col_result:
        if submit_btn:
            # --- GỌI BỘ NÃO LÀM VIỆC ---
            analyzer = AssetLocationAnalyzer(tax_bracket=tax_rate/100)
            result = analyzer.analyze(asset_type, amount, years)
            
            # --- HIỂN THỊ KẾT QUẢ ---
            st.subheader("💡 Kết Quả Phân Tích")
            
            # 1. Hiển thị thẻ màu khuyến nghị
            rec = result['recommendation']
            if "TAXABLE" in rec or "Thường" in rec:
                st.success(f"✅ **KHUYẾN NGHỊ:** {rec}")
            elif "DEFERRED" in rec or "Hoãn" in rec:
                st.warning(f"⚠️ **KHUYẾN NGHỊ:** {rec}")
            else:
                st.info(f"ℹ️ **KHUYẾN NGHỊ:** {rec}")
            
            # 2. Lý do chi tiết
            st.markdown(f"**🧐 Lý do:** {result['reason']}")
            
            # 3. Metric tiền tiết kiệm được
            st.markdown("---")
            col_metric1, col_metric2 = st.columns(2)
            with col_metric1:
                st.metric(
                    label="Đánh giá hiệu quả thuế",
                    value=result['profile']
                )
            with col_metric2:
                saved = result.get('saved_value', 0)
                st.metric(
                    label=f"Tiền 'né' được thuế sau {years} năm",
                    value=f"+ ${saved:,.2f}",
                    delta="Lợi nhuận ròng"
                )
                
        else:
            # Màn hình chờ
            st.info("👈 Vui lòng nhập thông tin bên trái để AI tính toán chiến lược thuế tối ưu.")
            with st.expander("📖 Xem bảng tra cứu nhanh"):
                st.table({
                    "Tài Sản": ["REITs / Crypto Trade", "Trái phiếu (Bonds)", "Cổ phiếu (Stocks)"],
                    "Độ 'Ngốn' Thuế": ["🔴 Rất Cao", "🟠 Trung Bình", "🟢 Thấp"],
                    "Nơi Nên Để": ["Ví Hưu Trí / Hoãn Thuế", "Ví Hưu Trí", "Ví Thường"]
                })

# === TAB 2: WHALE HUNTER ===
elif menu == "🐋 Whale Hunter (Sắp ra mắt)":
    st.empty()
    st.header("🚧 Khu Vực Đang Xây Dựng")
    st.warning("Module Săn Cá Mập đang được bảo trì để nâng cấp giao diện mới.")
    st.image("https://media.giphy.com/media/l0HlHJGHe3yAMhdQY/giphy.gif", width=400) # Ảnh vui nhộn

# === TAB 3: SETTINGS ===
elif menu == "⚙️ Cài Đặt":
    st.header("⚙️ Cấu Hình Hệ Thống")
    st.write("Phiên bản Core: v1.0.2")
    st.write("Kết nối API: 🔴 Disconnected")
