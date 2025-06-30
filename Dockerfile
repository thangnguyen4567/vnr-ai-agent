FROM python:3.10-slim

WORKDIR /app

# Cài đặt các thư viện cần thiết
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn
COPY . .

# Expose cổng cho API và Streamlit
EXPOSE 8000 8501

# Thiết lập biến môi trường mặc định
ENV PYTHONPATH=/app

# Command để chạy ứng dụng (có thể overwrite bằng docker-compose)
CMD ["python", "src/main.py"] 