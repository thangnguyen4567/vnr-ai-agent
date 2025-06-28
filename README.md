# AI Core Framework

Framework xử lý và phát triển các ứng dụng AI.

## Cài đặt môi trường

### Tạo môi trường ảo
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python -m venv venv
source venv/bin/activate
```

### Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### Cài đặt package trong chế độ phát triển
```bash
pip install -e .
```

## Cấu hình môi trường
1. Sao chép file `.env.example` thành `.env`
2. Chỉnh sửa các biến môi trường trong `.env` theo yêu cầu của bạn

## Cấu trúc dự án
```
AI/
  - core/               # Module core
    - __init__.py
    - edges/            # Xử lý các kết nối giữa các node
    - nodes/            # Các loại node trong framework
      - __init__.py
      - base_node.py
      - context_node/   # Node xử lý ngữ cảnh
      - llm_node/       # Node tích hợp các mô hình ngôn ngữ
      - router_node/    # Node điều hướng
      - tool_node/      # Node công cụ
      - utils/          # Các tiện ích
  - api/                # Module API
    - app.py            # Định nghĩa ứng dụng FastAPI
    - main.py           # Điểm khởi chạy API
    - models/           # Các mô hình dữ liệu
    - routers/          # Các router API
    - services/         # Các service xử lý logic
```

## Sử dụng
(Thêm hướng dẫn sử dụng dự án sau khi đã hoàn thiện) 

## Chạy ứng dụng Streamlit

Để chạy ứng dụng Streamlit, hãy thực hiện các bước sau:

1. Đảm bảo bạn đã kích hoạt môi trường ảo và cài đặt tất cả các dependencies
2. Chạy lệnh sau trong terminal:

```bash
streamlit run app.py
```

## Chạy API

### Khởi động API

Để khởi động API FastAPI, hãy thực hiện lệnh sau:

```bash
python -m src.api.main
```

API sẽ khởi động ở địa chỉ http://localhost:8000

### Tài liệu API

FastAPI cung cấp tài liệu API được tạo tự động:

1. **Swagger UI** - Giao diện tương tác để thử nghiệm các endpoint API:
   - URL: http://localhost:8000/docs
   - Tính năng: Cho phép gửi yêu cầu, xem phản hồi và kiểm tra schema

2. **ReDoc** - Tài liệu API có thiết kế đẹp và thân thiện với người đọc:
   - URL: http://localhost:8000/redoc
   - Tính năng: Hiển thị tài liệu rõ ràng, dễ đọc, không có chức năng thử nghiệm

### Các API endpoint

Dự án hiện có các endpoint sau:

- **GET /** - Endpoint gốc với thông báo chào mừng
- **GET /health** - Kiểm tra trạng thái hoạt động của API
- **GET /health/details** - Chi tiết về trạng thái hệ thống và tài nguyên
- **POST /ai/process** - Xử lý yêu cầu AI