# AI Core Framework

Framework xử lý và phát triển các ứng dụng AI.

## Cài đặt môi trường

### Yêu cầu
- Python 3.9 trở lên
- pip

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