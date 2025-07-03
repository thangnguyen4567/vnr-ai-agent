# VNR AI Agent Platform

Nền tảng xây dựng và vận hành AI Agent với LangGraph và LangChain, giúp phát triển và triển khai các hệ thống AI thông minh.

## 🚀 Tính năng chính

- **Multi-Agent Framework**: Xây dựng hệ thống đa agent với LangGraph
- **Giao diện Streamlit**: Tương tác trực quan với agent qua giao diện chat
- **API FastAPI**: Tích hợp agent vào các ứng dụng thông qua RESTful API
- **Giám sát với Langfuse**: Theo dõi và phân tích hiệu suất agent trong thời gian thực
- **Lưu trữ trạng thái**: Hỗ trợ checkpointing với MongoDB

## 🔧 Cài đặt

### Yêu cầu

- Python 3.11+ (khuyên dùng Python 3.13)
- MongoDB (cơ sở dữ liệu để lưu trữ checkpointing)
- API key cho các LLM (OpenAI, Google AI, Anthropic)

### Cài đặt trực tiếp

1. Tạo và kích hoạt môi trường ảo:

```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate
```

2. Cài đặt các thư viện phụ thuộc:

```bash
pip install -r requirements.txt
```

3. Cài đặt package trong chế độ phát triển:

```bash
pip install -e .
```

### Cài đặt với Docker

```bash
# Khởi chạy toàn bộ hệ thống (bao gồm MongoDB và Langfuse)
docker-compose up -d

# Chỉ khởi chạy dịch vụ AI Agent
docker-compose up ai-agent -d
```

## ⚙️ Cấu hình

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

Hệ thống sử dụng MongoDB để lưu trữ checkpointer của LangGraph, giúp lưu trữ trạng thái của agent trong quá trình thực thi.

**Cài đặt MongoDB:**
- **Windows**: [Hướng dẫn cài đặt MongoDB trên Windows](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-windows/)
- **Mac**: [Hướng dẫn cài đặt MongoDB trên macOS](https://www.mongodb.com/docs/manual/tutorial/install-mongodb-on-os-x/)
- **Linux**: [Hướng dẫn cài đặt MongoDB trên Linux](https://www.mongodb.com/docs/manual/administration/install-on-linux/)

**Hoặc sử dụng MongoDB Atlas:**
1. Tạo tài khoản tại [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
2. Tạo một cluster mới
3. Nhận connection string và thiết lập trong biến môi trường `MONGODB_URI`

### Langfuse Analytics

Hệ thống tích hợp Langfuse để theo dõi, phân tích và đánh giá hiệu suất của các agent AI:

- **Trong Docker**: Langfuse được cài đặt tự động
- **Cài đặt trực tiếp**:
  1. Tạo tài khoản tại [Langfuse](https://langfuse.com)
  2. Lấy API key và cập nhật biến môi trường

**Thông tin đăng nhập Langfuse mặc định:**
- Email: admin@admin.com
- Mật khẩu: Vnr@1234

## 🏃‍♂️ Chạy ứng dụng

### Chạy Streamlit UI

```bash
streamlit run app.py
```

Truy cập giao diện web tại: http://localhost:8501

### Chạy API Server

```bash
# Cách 1
python -m src.main

# Cách 2
uvicorn src.api.app:app --host 0.0.0.0 --port 8000 --reload
```

API sẽ khởi động tại: http://localhost:8000

### Tài liệu API

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 📁 Cấu trúc dự án

```
├── app.py                  # Ứng dụng Streamlit
├── src/
│   ├── api/                # FastAPI endpoints
│   │   ├── app.py          # Định nghĩa ứng dụng FastAPI
│   │   ├── models/         # Các model Pydantic
│   │   ├── routers/        # API routes
│   │   └── services/       # Logic xử lý API
│   ├── core/               # LangGraph core
│   │   ├── nodes/          # Các node trong graph
│   │   ├── edges/          # Kết nối giữa các node
│   │   ├── tools/          # Công cụ cho agent
│   │   ├── fc_agent.py     # Định nghĩa function calling agent
│   │   ├── multi_agent.py  # Định nghĩa multi agent
│   │   └── config_loader.py # Bộ nạp cấu hình
│   ├── utils/              # Tiện ích
│   └── main.py             # Entry point
├── docker-compose.yml      # Cấu hình Docker
├── Dockerfile              # Định nghĩa Docker image
└── requirements.txt        # Thư viện phụ thuộc
```

## 📚 API Endpoints

- **GET /** - Endpoint gốc với thông báo chào mừng
- **GET /health** - Kiểm tra trạng thái hoạt động của API
- **GET /health/details** - Chi tiết về trạng thái hệ thống và tài nguyên
- **POST /ai/process** - Xử lý yêu cầu AI

## 🔍 Debug

Để debug ứng dụng trong Docker:
1. Ứng dụng có cấu hình sẵn debugpy port 5678
2. Kết nối với debugger thông qua VS Code