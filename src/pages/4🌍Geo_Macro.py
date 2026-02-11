# pages/4_🌍_Geo_Macro.py
import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

st.title("Global Macro & Supply Chain Intelligence 🌍")

st.markdown("""
Dashboard này mô phỏng luồng hàng hóa và rủi ro địa chính trị. 
Dữ liệu hiển thị bên dưới là dữ liệu mẫu mô phỏng các tuyến đường vận tải biển huyết mạch (Maritime Choke Points).
""")

# Dữ liệu mô phỏng: Các cảng lớn và khối lượng vận chuyển
# Trong thực tế, dữ liệu này nên được lấy từ API vệ tinh (AIS Data)
ports_data = pd.DataFrame({
    'port_name':,
    'lat': [31.2304, 1.3521, 51.9244, 33.7450, 25.2048, 40.7128],
    'lon': [121.4737, 103.8198, 4.4777, -118.2600, 55.2708, -74.0060],
    'volume': , # Đơn vị giả định: nghìn TEU
    'risk_level': [0.2, 0.1, 0.1, 0.3, 0.4, 0.1] # Mức độ rủi ro địa chính trị (0-1)
})

# Dữ liệu mô phỏng: Tuyến đường (Arcs)
# Kết nối từ Shanghai đi các nơi
routes_data = pd.DataFrame({
    'source_lon': [121.4737, 121.4737, 121.4737],
    'source_lat': [31.2304, 31.2304, 31.2304],
    'target_lon': [-118.2600, 4.4777, 103.8198],
    'target_lat': [33.7450, 51.9244, 1.3521],
    'value': 
})

# Cấu hình Layer PyDeck

# 1. Arc Layer: Thể hiện tuyến đường vận chuyển
arc_layer = pdk.Layer(
    "ArcLayer",
    data=routes_data,
    get_source_position=["source_lon", "source_lat"],
    get_target_position=["target_lon", "target_lat"],
    get_width="value / 10",
    get_source_color=,
    get_target_color=,
    get_tilt=15,
)

# 2. Column Layer: Thể hiện khối lượng hàng hóa tại cảng (3D Bars)
column_layer = pdk.Layer(
    "ColumnLayer",
    data=ports_data,
    get_position=["lon", "lat"],
    get_elevation="volume * 100",
    elevation_scale=50,
    radius=150000,
    get_fill_color=,
    pickable=True,
    auto_highlight=True,
)

# 3. Scatterplot Layer: Thể hiện rủi ro (Vòng tròn đỏ cảnh báo)
risk_layer = pdk.Layer(
    "ScatterplotLayer",
    data=ports_data[ports_data['risk_level'] > 0.3],
    get_position=["lon", "lat"],
    get_color=,
    get_radius="risk_level * 500000",
    opacity=0.5,
    stroked=True,
    filled=False,
    line_width_min_pixels=2,
)

# View State: Góc nhìn camera ban đầu
view_state = pdk.ViewState(
    latitude=20,
    longitude=10,
    zoom=1,
    pitch=45,
)

# Render Bản đồ
r = pdk.Deck(
    layers=[arc_layer, column_layer, risk_layer],
    initial_view_state=view_state,
    map_style="mapbox://styles/mapbox/dark-v10",
    tooltip={"text": "{port_name}\nVolume: {volume}\nRisk: {risk_level}"}
)

st.pydeck_chart(r)

st.info("💡 Insight: Các cột màu cam thể hiện khối lượng hàng hóa, các cung tròn là tuyến đường vận tải. Vòng tròn đỏ nhấp nháy cảnh báo khu vực có rủi ro địa chính trị cao ảnh hưởng đến chuỗi cung ứng.")
