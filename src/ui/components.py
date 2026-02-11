"""
=============================================================================
PROJECT: FINCEPT TERMINAL CORE
FILE: src/ui/components.py
ROLE: UI Components & Advanced Charting Engine
AUTHOR: Fincept Copilot (Emo)
=============================================================================
"""

import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from typing import Optional

class TerminalUI:
    """Kho giao diện dùng chung cho toàn bộ Terminal"""

    @staticmethod
    def render_metric_card(label: str, value: float, change_pct: float, prefix: str = "$", format_str: str = "{:,.2f}"):
        """
        Render thẻ chỉ số tài chính thông minh, tự đổi màu theo biến động.
        """
        # Nếu change_pct = 0, hiện màu xám (off). Lớn hơn 0 hiện xanh (normal), Nhỏ hơn 0 hiện đỏ (inverse)
        color = "off"
        if change_pct > 0:
            color = "normal"
        elif change_pct < 0:
            color = "inverse"
            
        st.metric(
            label=label, 
            value=f"{prefix}{format_str.format(value)}", 
            delta=f"{change_pct:+.2f}%", 
            delta_color=color
        )

    @staticmethod
    def render_advanced_chart(df: pd.DataFrame, title: str, show_volume: bool = True):
        """
        Động cơ vẽ biểu đồ tài chính đẳng cấp Enterprise bằng Plotly.
        - Tự động bỏ qua các ngày nghỉ cuối tuần (không bị rỗng nến).
        - Tích hợp Volume (Khối lượng) ngay bên dưới đồ thị giá.
        - Hỗ trợ vẽ các đường MA (Moving Average) nếu có trong DataFrame.
        """
        if df is None or df.empty:
            st.warning("SYSTEM ALERT: No sufficient data available for charting.")
            return

        # 1. Khởi tạo Subplots: Hàng 1 cho Giá (chiếm 80%), Hàng 2 cho Khối lượng (chiếm 20%)
        if show_volume and 'Volume' in df.columns:
            fig = make_subplots(
                rows=2, cols=1, 
                shared_xaxes=True, 
                vertical_spacing=0.03, 
                row_heights=[0.8, 0.2]
            )
        else:
            fig = make_subplots(rows=1, cols=1)

        # 2. Thêm đồ thị nến (Candlestick)
        fig.add_trace(
            go.Candlestick(
                x=df['timestamp'],
                open=df['Open'],
                high=df['High'],
                low=df['Low'],
                close=df['Close'],
                increasing_line_color='#00FFAA', # Xanh Neon (Bullish)
                decreasing_line_color='#FF4444', # Đỏ Crimson (Bearish)
                name='Price Action'
            ),
            row=1, col=1
        )

        # 3. Quét và thêm các đường Trung bình động (Moving Averages) nếu tồn tại trong DF
        # (Chúng ta sẽ tính toán các cột này ở module technical.py sau)
        colors_ma = {'SMA_20': '#FFA500', 'SMA_50': '#1E90FF', 'SMA_200': '#FF1493', 'EMA_12': '#00FFFF', 'EMA_26': '#FFD700'}
        for col_name, color_hex in colors_ma.items():
            if col_name in df.columns:
                fig.add_trace(
                    go.Scatter(
                        x=df['timestamp'], y=df[col_name], 
                        line=dict(color=color_hex, width=1.5), 
                        name=col_name.replace('_', ' ')
                    ),
                    row=1, col=1
                )

        # 4. Thêm biểu đồ Khối lượng (Volume)
        if show_volume and 'Volume' in df.columns:
            # Màu cột volume trùng với màu nến của ngày hôm đó
            volume_colors = ['#00FFAA' if row['Close'] >= row['Open'] else '#FF4444' for _, row in df.iterrows()]
            fig.add_trace(
                go.Bar(
                    x=df['timestamp'], 
                    y=df['Volume'], 
                    marker_color=volume_colors, 
                    name='Volume',
                    opacity=0.8
                ),
                row=2, col=1
            )

        # 5. Tùy chỉnh Layout chuẩn Terminal
        fig.update_layout(
            title=dict(text=f"<b>{title}</b>", font=dict(family="Roboto Mono", size=20, color="#FAFAFA")),
            template='plotly_dark',
            margin=dict(l=10, r=10, t=50, b=10),
            height=650, # Chiều cao tối ưu cho màn hình Desktop
            paper_bgcolor='rgba(0,0,0,0)', # Nền trong suốt để tiệp với Streamlit Dark Mode
            plot_bgcolor='rgba(14, 17, 23, 0.5)',
            xaxis_rangeslider_visible=False, # Tắt thanh cuộn dưới đáy để nhìn chuyên nghiệp hơn
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                font=dict(color="#8892B0")
            )
        )

        # 6. Loại bỏ khoảng trống cuối tuần trên trục X (Hide weekend gaps)
        # Chỉ áp dụng nếu dữ liệu là ngày (nhỏ hơn 300 điểm dữ liệu thường là daily)
        if len(df) > 0 and 'timestamp' in df.columns:
            # Lấy danh sách các ngày không có giao dịch (ví dụ T7, CN)
            dt_all = pd.date_range(start=df['timestamp'].iloc[0], end=df['timestamp'].iloc[-1])
            dt_obs = [d.strftime("%Y-%m-%d") for d in df['timestamp']]
            dt_breaks = [d for d in dt_all.strftime("%Y-%m-%d").tolist() if not d in dt_obs]
            
            fig.update_xaxes(rangebreaks=[dict(values=dt_breaks)])

        # Cập nhật định dạng trục
        fig.update_yaxes(title_text="Price (USD)", row=1, col=1, gridcolor='#262730', zerolinecolor='#262730')
        if show_volume:
            fig.update_yaxes(title_text="Volume", row=2, col=1, showgrid=False)

        # Render ra Streamlit
        st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False}) # Tắt thanh công cụ của Plotly cho gọn

    @staticmethod
    def render_data_table(df: pd.DataFrame, height: int = 400):
        """Hiển thị bảng dữ liệu (Dataframe) với định dạng số chuẩn"""
        if df is None or df.empty:
            return
            
        # Format số thập phân cho đẹp
        formatted_df = df.copy()
        for col in formatted_df.select_dtypes(include=['float64', 'float32']).columns:
            formatted_df[col] = formatted_df[col].apply(lambda x: f"{x:,.2f}" if pd.notnull(x) else "N/A")
            
        st.dataframe(formatted_df, height=height, use_container_width=True)
