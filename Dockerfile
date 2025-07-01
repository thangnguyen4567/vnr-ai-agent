FROM python:3.13-slim

# Cài đặt Git
RUN apt-get update && apt-get install -y git

# RUN apt-get update && apt-get install -y \
#     curl \
#     apt-transport-https \
#     gnupg \
#     unixodbc \
#     unixodbc-dev \
#     && rm -rf /var/lib/apt/lists/*

# RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
#     RUN curl https://packages.microsoft.com/config/ubuntu/18.04/prod.list > /etc/apt/sources.list.d/mssql-release.list
#     RUN apt-get update
#     RUN ACCEPT_EULA=Y apt-get install -y --allow-unauthenticated msodbcsql17
#     RUN apt install ffmpeg -y

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose cổng cho API và Streamlit
EXPOSE 8000 8501

# Thiết lập biến môi trường mặc định
ENV PYTHONPATH=/app

# Command để chạy ứng dụng (có thể overwrite bằng docker-compose)
CMD ["python", "src/main.py"] 