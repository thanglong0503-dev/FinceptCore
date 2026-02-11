import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from utils.data_fetcher import MarketDataEngine

st.title("🧮 Mô Hình Định Giá Chiết Khấu Dòng Tiền (DCF)")
st.caption("Institutional Valuation Model v1.0 | Fincept Quantitative Core")

# 1. Nhập liệu & Giả định (Inputs & Assumptions)
ticker = st.session_state.current_ticker
st.subheader(f"Phân tích Định giá cho: {ticker}")

data = MarketDataEngine.get_fundamental_info(ticker)

if data and not data['cashflow'].empty:
    col1, col2, col3 = st.columns(3)
    
    # Tự động trích xuất dữ liệu tài chính (Financial Extraction Logic)
    try:
        # Lấy dòng tiền tự do gần nhất (Free Cash Flow)
        fcf_series = data['cashflow'].loc['Free Cash Flow']
        # Xử lý nếu dữ liệu trả về bị đảo ngược thời gian
        latest_fcf = fcf_series.iloc 
        
        # Tổng nợ và Tiền mặt để tính Equity Value từ Enterprise Value
        balance_sheet = data['balance_sheet']
        # Sử dụng.get() để tránh lỗi KeyError nếu báo cáo thiếu mục
        total_debt = balance_sheet.loc.iloc if 'Total Debt' in balance_sheet.index else 0
        cash_equivalents = balance_sheet.loc['Cash And Cash Equivalents'].iloc if 'Cash And Cash Equivalents' in balance_sheet.index else 0
        
        shares_outstanding = data['info'].get('sharesOutstanding', 1)
        beta = data['info'].get('beta', 1.0)
        
        # Kiểm tra tính hợp lệ của dữ liệu
        if shares_outstanding is None: shares_outstanding = 1
        if beta is None: beta = 1.0
        
    except Exception as e:
        st.error(f"Dữ liệu tài chính không đủ để tự động điền: {e}")
        st.stop()

    # Giao diện nhập tham số mô hình
    with col1:
        st.markdown("### 1. Giả định Tăng trưởng")
        growth_rate_1_5 = st.slider("Tăng trưởng FCF (Năm 1-5)", -20.0, 50.0, 10.0, 0.5, format="%.1f%%") / 100
        growth_rate_6_10 = st.slider("Tăng trưởng FCF (Năm 6-10)", -20.0, 30.0, 5.0, 0.5, format="%.1f%%") / 100
        terminal_growth = st.number_input("Tăng trưởng Dài hạn (g)", 0.0, 6.0, 2.5, 0.1) / 100
        st.caption("Lưu ý: g không nên lớn hơn tốc độ tăng trưởng GDP.")

    with col2:
        st.markdown("### 2. Chi phí Vốn (WACC)")
        risk_free_rate = st.number_input("Lãi suất Phi rủi ro (Rf)", 0.0, 10.0, 4.2) / 100
        market_return = st.number_input("Lợi nhuận Thị trường Kỳ vọng (Rm)", 5.0, 20.0, 9.0) / 100
        
        # Tính Cost of Equity theo mô hình CAPM: Ke = Rf + Beta * (Rm - Rf)
        cost_of_equity = risk_free_rate + beta * (market_return - risk_free_rate)
        st.info(f"Cost of Equity (CAPM): {cost_of_equity:.2%}")
        
        # Cho phép người dùng điều chỉnh WACC cuối cùng
        wacc = st.slider("WACC Ước tính %", 5.0, 20.0, float(cost_of_equity * 100), 0.1) / 100

    with col3:
        st.markdown("### 3. Thông số Hiện tại")
        st.metric("FCF Gần nhất (Tỷ USD)", f"${latest_fcf/1e9:.2f}B")
        st.metric("Nợ Ròng (Net Debt)", f"${(total_debt - cash_equivalents)/1e9:.2f}B")
        st.metric("Hệ số Beta", f"{beta:.2f}")

    # -------------------------------------------------------------------------
    # 2. Động cơ Dự phóng (Projection Engine)
    # -------------------------------------------------------------------------
    future_fcf =
    discount_factors =
    discounted_fcf =
    
    # Dự phóng Năm 1-10
    current_fcf_proj = latest_fcf
    for i in range(1, 11):
        rate = growth_rate_1_5 if i <= 5 else growth_rate_6_10
        current_fcf_proj = current_fcf_proj * (1 + rate)
        future_fcf.append(current_fcf_proj)
        
        # Hệ số chiết khấu: 1 / (1 + WACC)^t
        df = 1 / ((1 + wacc) ** i)
        discount_factors.append(df)
        discounted_fcf.append(current_fcf_proj * df)

    # Tính Giá trị Kết dư (Terminal Value)
    # Công thức Gordon Growth: TV = (FCF_n * (1 + g)) / (WACC - g)
    if wacc <= terminal_growth:
        st.error("Lỗi: WACC phải lớn hơn tốc độ tăng trưởng dài hạn (g).")
        st.stop()
        
    terminal_value = (future_fcf[-1] * (1 + terminal_growth)) / (wacc - terminal_growth)
    discounted_tv = terminal_value / ((1 + wacc) ** 10)

    # Tổng hợp Giá trị Doanh nghiệp (Enterprise Value)
    sum_pv_fcf = sum(discounted_fcf)
    enterprise_value = sum_pv_fcf + discounted_tv
    
    # Chuyển đổi sang Giá trị Vốn chủ sở hữu (Equity Value)
    equity_value = enterprise_value - total_debt + cash_equivalents
    implied_share_price = equity_value / shares_outstanding
    
    current_price = data['info'].get('currentPrice', 0)
    upside = ((implied_share_price - current_price) / current_price) * 100

    # -------------------------------------------------------------------------
    # 3. Trực quan hóa Kết quả (Visualization)
    # -------------------------------------------------------------------------
    st.divider()
    st.header("Kết Quả Định Giá")
    
    # Hiển thị Metrics chính
    res_col1, res_col2, res_col3 = st.columns(3)
    res_col1.metric("Giá Trị Nội Tại (Implied Price)", f"${implied_share_price:.2f}", 
                    delta=f"{upside:.2f}% so với Hiện tại ({current_price})")
    res_col2.metric("Enterprise Value", f"${enterprise_value/1e9:.2f}B")
    res_col3.metric("Tỷ trọng Terminal Value", f"{(discounted_tv/enterprise_value)*100:.1f}%")

    # Biểu đồ Thác nước (Waterfall Chart) - Đặc trưng của báo cáo tài chính
    # [20, 21]
    fig = go.Figure(go.Waterfall(
        name = "DCF Breakdown", orientation = "v",
        measure = ["relative"] * 10 + ["relative", "total"],
        x = [f"Năm {i}" for i in range(1, 11)] +,
        textposition = "outside",
        text = +,
        y = discounted_fcf + [discounted_tv, 0],
        connector = {"line":{"color":"rgb(63, 63, 63)"}},
        decreasing = {"marker":{"color":"#ef553b"}},
        increasing = {"marker":{"color":"#00cc96"}},
        totals = {"marker":{"color":"#636efa"}}
    ))
    
    fig.update_layout(
        title="Phân rã Giá trị Doanh nghiệp (Waterfall Analysis)",
        template="plotly_dark",
        yaxis_title="Giá trị Hiện tại (PV) - USD",
        showlegend = False,
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

    # Phân tích Độ nhạy (Sensitivity Analysis) - Bảng ma trận
    # Đây là yêu cầu bắt buộc đối với báo cáo tài chính chuyên nghiệp
    st.subheader("Phân tích Độ nhạy: WACC vs Terminal Growth")
    st.markdown("Bảng dưới đây cho thấy giá cổ phiếu thay đổi như thế nào khi các giả định đầu vào thay đổi.")
    
    # Tạo ma trận WACC +/- 1% và Growth +/- 0.5%
    wacc_steps = np.linspace(wacc - 0.01, wacc + 0.01, 5)
    growth_steps = np.linspace(terminal_growth - 0.005, terminal_growth + 0.005, 5)
    
    sensitivity_data =
    for w in wacc_steps:
        row =
        for g in growth_steps:
            if w <= g:
                row.append(0) # Tránh chia cho 0 hoặc âm
                continue
            tv_sens = (future_fcf[-1] * (1 + g)) / (w - g)
            dtv_sens = tv_sens / ((1 + w) ** 10)
            ev_sens = sum([f / ((1+w)**(i+1)) for i, f in enumerate(future_fcf)]) + dtv_sens
            price_sens = (ev_sens - total_debt + cash_equivalents) / shares_outstanding
            row.append(price_sens)
        sensitivity_data.append(row)
        
    df_sens = pd.DataFrame(sensitivity_data, 
                           index=,
                           columns=[f"Growth {g:.2%}" for g in growth_steps])
    
    # Tô màu bảng (Heatmap styling)
    st.dataframe(df_sens.style.background_gradient(cmap='RdYlGn', axis=None).format("${:.2f}"), 
                 use_container_width=True)

else:
    st.error("Không có dữ liệu dòng tiền (Cashflow) cho mã cổ phiếu này để chạy DCF.")
