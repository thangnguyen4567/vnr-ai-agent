# Agent AI Platform

Nền tảng xây dựng và chạy AI Agent với LangGraph và LangChain.

## Cấu hình

### Biến môi trường

Tạo file `.env` ở thư mục gốc với các biến môi trường sau:

```
# Cấu hình MongoDB
MONGODB_URI=mongodb://localhost:27017

# Cấu hình LLMs
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Langfuse
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://us.cloud.langfuse.com
LANGFUSE_SESSION_ID=default-session
```

### MongoDB Checkpointer

Hệ thống sử dụng MongoDB để lưu trữ checkpointer của LangGraph, giúp lưu trữ trạng thái của agent trong quá trình thực thi. Hãy đảm bảo MongoDB đã được cài đặt và chạy trước khi khởi động ứng dụng.

Để cài đặt MongoDB:
- **Windows**: [Hướng dẫn cài đặt MongoDB trên Windows](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
- **Mac**: [Hướng dẫn cài đặt MongoDB trên macOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
- **Linux**: [Hướng dẫn cài đặt MongoDB trên Linux](https://www.mongodb.com/docs/manual/administration/install-on-linux/)

Hoặc sử dụng MongoDB Atlas (đám mây):
1. Tạo tài khoản tại [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Tạo một cluster mới
3. Nhận connection string và thiết lập trong biến môi trường `MONGODB_URI`

### Langfuse Analytics

Hệ thống sử dụng Langfuse để theo dõi, phân tích và đánh giá hiệu suất của các agent AI. Langfuse là một nền tảng quan sát chuyên dụng cho các ứng dụng AI.

Trong môi trường Docker, Langfuse được cài đặt tự động để lưu trữ dữ liệu. Đối với cài đặt trực tiếp, bạn có thể:

1. Tạo tài khoản tại [Langfuse](https://langfuse.com)
2. Lấy API key (public và secret)
3. Cập nhật các biến môi trường:
   ```
   LANGFUSE_PUBLIC_KEY=pk-lf-your_public_key
   LANGFUSE_SECRET_KEY=sk-lf-your_secret_key
   LANGFUSE_HOST=https://us.cloud.langfuse.com
   LANGFUSE_SESSION_ID=your-session-id
   ```

## Chạy ứng dụng

### Chạy trực tiếp

1. Cài đặt dependencies:
```
pip install -r requirements.txt
```

2. Chạy ứng dụng:
```
python src/main.py
```

3. Chạy API Server:
```
uvicorn src.api.app:app --reload
```

### Chạy với Docker

Chúng tôi cung cấp Docker Compose để dễ dàng khởi chạy toàn bộ hệ thống, bao gồm MongoDB và Langfuse.

1. Đảm bảo bạn đã cài đặt [Docker](https://www.docker.com/get-started) và [Docker Compose](https://docs.docker.com/compose/install/).

2. Khởi chạy toàn bộ hệ thống:
```bash
docker-compose up
```

3. Hoặc chạy từng service riêng biệt:
```bash
docker-compose up mongodb  # Chỉ chạy MongoDB
docker-compose up langfuse  # Chỉ chạy Langfuse
docker-compose up api      # Chỉ chạy API Server
docker-compose up streamlit # Chỉ chạy Streamlit UI
```

4. Truy cập các services:
   - MongoDB: mongodb://localhost:27017 (username: admin, password: adminpassword)
   - Langfuse UI: http://localhost:3000
   - API Server: http://localhost:8000
   - Streamlit UI: http://localhost:8501

5. Để biết thêm chi tiết về cài đặt Docker, hãy xem file [docker-setup.md](docker-setup.md).

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

## Chạy ứng dụng chính

Để chạy ứng dụng AI chính, có các cách sau:

1. Chạy từ thư mục gốc của dự án:
```bash
# Cách 1
python -m src.main

# Cách 2
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```

2. Nếu bạn gặp lỗi, hãy đảm bảo đã cài đặt các dependencies:
```bash
pip install -r requirements.txt
python -m src.main
```

Ứng dụng sẽ khởi động API và chạy trên cổng 8000: http://localhost:8000

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