# Hướng dẫn cài đặt Docker

## Chuẩn bị môi trường

1. **Tạo file `.env` ở thư mục gốc:**

```
# API Keys cho LLMs
OPENAI_API_KEY=your_openai_api_key
GOOGLE_API_KEY=your_google_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key

# Langfuse
LANGFUSE_PUBLIC_KEY=your_langfuse_public_key
LANGFUSE_SECRET_KEY=your_langfuse_secret_key
LANGFUSE_HOST=https://us.cloud.langfuse.com
LANGFUSE_SESSION_ID=default-session
```

2. **Thay thế các giá trị API key của bạn vào file .env**

## Khởi chạy Docker Compose

### Khởi động toàn bộ hệ thống

```bash
docker-compose up
```

### Khởi động từng service riêng biệt

#### Chỉ khởi động MongoDB:
```bash
docker-compose up mongodb
```

#### Chỉ khởi động Langfuse:
```bash
docker-compose up langfuse
```

#### Chỉ khởi động API server:
```bash
docker-compose up api
```

#### Chỉ khởi động Streamlit UI:
```bash
docker-compose up streamlit
```

## Truy cập các services

- **MongoDB**: mongodb://localhost:27017 (username: admin, password: adminpassword)
- **Langfuse**: http://localhost:3000
- **API Server**: http://localhost:8000

## Cấu trúc Docker

1. **MongoDB**: Lưu trữ checkpointer cho LangGraph
2. **Langfuse**: Nền tảng quan sát, phân tích và đánh giá cho ứng dụng AI (sử dụng SQLite tích hợp)
3. **API Server**: Chạy FastAPI để cung cấp API

## Quản lý dữ liệu

Dữ liệu được lưu trữ trong các volume Docker để đảm bảo không bị mất khi container bị xóa:
- **mongodb_data**: Lưu trữ dữ liệu MongoDB
- **langfuse_data**: Lưu trữ dữ liệu SQLite của Langfuse

## Sử dụng Langfuse

Langfuse là nền tảng quan sát, phân tích và đánh giá cho ứng dụng AI. Để sử dụng Langfuse:

1. Truy cập Langfuse UI tại http://localhost:3000
2. Đăng ký tài khoản người dùng mới
3. Tạo project mới
4. Lấy API key và cập nhật trong docker-compose.yml:
   ```yaml
   environment:
     - LANGFUSE_PUBLIC_KEY=pk-lf-your_public_key
     - LANGFUSE_SECRET_KEY=sk-lf-your_secret_key
   ```

## Sửa đổi cấu hình MongoDB

Nếu bạn muốn thay đổi thông tin đăng nhập MongoDB, hãy cập nhật các biến sau trong docker-compose.yml:

1. Trong phần `mongodb > environment`:
   - MONGO_INITDB_ROOT_USERNAME
   - MONGO_INITDB_ROOT_PASSWORD

2. Trong phần `api > environment` và `streamlit > environment` cập nhật:
   - MONGODB_URI=mongodb://username:password@mongodb:27017 