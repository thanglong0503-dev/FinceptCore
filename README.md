# FinceptCore
Enterprise-grade Financial Intelligence Platform built with Python &amp; Streamlit. Features: On-chain Whale Tracking, CFA Analytics, and AI Market Agents.

<img width="702" height="581" alt="image" src="https://github.com/user-attachments/assets/6489225c-7d5c-4308-9089-6105bf8cd1c9" />

2.1. Cây Thư mục Dự án (Project Directory Tree)
Fincept_Python_Terminal/
├──.streamlit/                   # Cấu hình giao diện và server Streamlit
│   ├── config.toml               # File cấu hình theme (Dark mode), server port
│   └── secrets.toml              # Lưu trữ API Keys (OpenAI, FMP, v.v.)
├── data/                         # Thư mục lưu trữ dữ liệu cục bộ (nếu cần)
│   ├── raw/                      # Dữ liệu thô tải về từ API
│   └── processed/                # Dữ liệu đã qua xử lý (Parquet/CSV)
├── src/                          # Mã nguồn chính (Source Code)
│   ├── init.py
│   ├── backend/                  # LỚP XỬ LÝ DỮ LIỆU (Data Layer)
│   │   ├── init.py
│   │   ├── api_client.py         # Module kết nối API tổng quát
│   │   ├── market_data.py        # Xử lý dữ liệu chứng khoán (Yahoo Finance)
│   │   ├── macro_data.py         # Xử lý dữ liệu vĩ mô (DBnomics)
│   │   └── alternative_data.py   # Dữ liệu thay thế (News, Crypto)
│   ├── analytics/                # LỚP PHÂN TÍCH (Logic Layer)
│   │   ├── init.py
│   │   ├── technical.py          # Phân tích kỹ thuật (RSI, MACD, BB)
│   │   ├── fundamental.py        # Phân tích cơ bản (DCF, Ratios)
│   │   └── portfolio.py          # Tối ưu hóa danh mục đầu tư
│   ├── ai/                       # LỚP TRÍ TUỆ NHÂN TẠO (AI Layer)
│   │   ├── init.py
│   │   ├── agent_core.py         # Khởi tạo LangChain Agent
│   │   ├── tools.py              # Định nghĩa công cụ (Tools) cho Agent
│   │   └── prompts.py            # Quản lý các Prompt Template
│   └── ui/                       # LỚP GIAO DIỆN (Presentation Layer)
│       ├── init.py
│       ├── components.py         # Các thành phần UI tái sử dụng (Card, Header)
│       ├── charts.py             # Hàm vẽ biểu đồ (Plotly, PyDeck)
│       └── layouts.py            # Cấu trúc bố cục trang
├── pages/                        # CÁC TRANG CỦA ỨNG DỤNG (Streamlit Pages)
│   ├── 1_📈Market_Dashboard.py  # Bảng điều khiển thị trường
│   ├── 2🔍Deep_Reseach.py      # Nghiên cứu chuyên sâu
│   ├── 3🤖AI_Copilot.py        # Trợ lý AI
│   ├── 4🌍Geo_Macro.py         # Bản đồ vĩ mô & địa chính trị
│   └── 5⚙️_Settings.py          # Cài đặt hệ thống
├── app.py                        # ĐIỂM KHỞI CHẠY (Entry Point)
├── requirements.txt              # Danh sách thư viện phụ thuộc
└── README.md                     # Tài liệu hướng dẫn
