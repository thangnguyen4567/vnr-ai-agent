# VNR AI Agent Platform

Nền tảng xây dựng và vận hành AI Agent với LangGraph và LangChain, giúp phát triển và triển khai các hệ thống AI thông minh.

## Kiến trúc 

https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/

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

Hệ thống cấu hình của VNR AI Agent Platform được quản lý thông qua các file YAML trong thư mục `settings/`:

- **settings/llm.yaml**: Cấu hình cho các mô hình ngôn ngữ lớn (LLM)
- **settings/multi_agent.yaml**: Định nghĩa cấu trúc và thuộc tính của hệ thống đa agent
- **settings/fc_agent.yaml**: Cấu hình cho function-calling agent
- **settings/mongodb.yaml**: Thông số kết nối đến MongoDB
- **settings/langfuse.yaml**: Cấu hình cho hệ thống giám sát Langfuse

Các file cấu hình được tải tự động khi khởi động ứng dụng bởi `ConfigReaderInstance` trong module `src.utils`. Người dùng có thể chỉnh sửa các file này để thay đổi hành vi của hệ thống AI Agent.

Để thêm mới hoặc cập nhật cấu hình:
1. Chỉnh sửa file cấu hình tương ứng trong thư mục `settings/`
2. Khởi động lại ứng dụng để áp dụng các thay đổi

### Cấu trúc file multi_agent.yaml

File `multi_agent.yaml` định nghĩa hệ thống đa agent với cấu trúc chi tiết như sau:

#### Thông tin cơ bản
```yaml
agent_id: "d4e12d5bb4014794fa3f956e2b0e01cf"  # ID duy nhất của multi agent
name: "Multi Agent"                            # Tên hiển thị
type: "multi"                                 # Loại agent (multi/fc)
```

#### Danh sách Agents
Mỗi agent được định nghĩa với ID riêng và mô tả chức năng:
```yaml
agents:
  - id: "f4e9a767bf49f68a77f7afd783665df9"    # ID duy nhất cho mỗi agent
    name: "Goal Agent"                        # Tên hiển thị
    description: "Agent tìm kiếm thông tin về mục tiêu KPI của phòng ban bộ phận" # Cần mô tả kỹ để AI phân tích chọn Agent phù hợp
```

#### Cấu hình Sub-agents
Mỗi sub-agent được định nghĩa chi tiết với:
```yaml
sub_agents:
  - agent_id: "f4e9a767bf49f68a77f7afd783665df9"  # ID tham chiếu đến agent trong danh sách
    name: "Goal Agent"                           # Tên hiển thị
    type: "fc"                                  # Loại agent (fc = function calling)
    nodes:
      llm:                                      # Cấu hình LLM cho agent này
        model: "gpt-4o-mini"                    # Mô hình LLM sử dụng
        temperature: 0.5                        # Độ sáng tạo (0-1)
        max_tokens: 1000                        # Giới hạn token đầu ra
        provider: "openai"                      # Nhà cung cấp LLM
        agent_prompt: ""                        # Prompt đặc biệt cho agent
```

#### Định nghĩa Tools
Mỗi agent có thể có nhiều tools, được chia làm 2 loại chính:

##### 1. Built-in Tools
Tools được định nghĩa sẵn trong code của hệ thống:
```yaml
tools:
  - type: built_in                            # Loại tool: built_in
    name: get_goal                            # Tên của tool
    description: "Lấy danh sách mục tiêu KPI của phòng ban bộ phận" # Mô tả
```

##### 2. HTTP Tools (API động)
Tools kết nối đến API bên ngoài:
```yaml
tools:
  - type: http                                # Loại tool: http
    name: get_weather                         # Tên của tool
    description: "Lấy thông tin thời tiết của thành phố"
    tool_path: https://api.open-meteo.com/v1/forecast  # Endpoint API
    
    # Các tham số đầu vào
    input_params:
      - name: latitude                        # Tên tham số
        description: "Vĩ độ"                  # Mô tả
        input_method: query                   # Phương thức truyền: query, header, path, body
        type: number                          # Kiểu dữ liệu
        default: 21.03                        # Giá trị mặc định
        
      - name: x-api-key                       # Ví dụ về tham số header
        description: "API key"
        input_method: header                  # Phương thức truyền: header
        type: string
        default: reqres-free-v1
    
    # Định nghĩa output
    output_params:
      - name: current_weather                 # Tên trường dữ liệu trả về
        type: string                          # Kiểu dữ liệu
        description: "Thời tiết hiện tại"     # Mô tả
```

#### Phương thức truyền Input Params
- **query**: Tham số được gửi qua query string trong URL (`?param=value`)
- **header**: Tham số được gửi trong header của request
- **path**: Tham số được truyền trong đường dẫn URL (`/api/{path_param}`)
- **body**: Tham số được gửi trong phần thân của request (JSON/form-data)

#### Output Params
Định nghĩa cấu trúc dữ liệu trả về, có thể là:
- **string**: Dữ liệu dạng chuỗi
- **number**: Dữ liệu dạng số
- **boolean**: Dữ liệu dạng boolean
- **json**: Dữ liệu dạng JSON phức tạp

Cấu trúc này cho phép hệ thống router định tuyến các câu hỏi của người dùng đến agent thích hợp và sử dụng các công cụ tương ứng để xử lý yêu cầu.

### Langfuse Analytics

Hệ thống tích hợp Langfuse để theo dõi, phân tích và đánh giá hiệu suất của các agent AI:

- **Trong Docker**: Langfuse được cài đặt tự động
- **Cài đặt trực tiếp**:
  1. Tạo tài khoản tại [Langfuse](https://langfuse.com)
  2. Lấy API key và cập nhật biến môi trường

**Thông tin đăng nhập Langfuse mặc định:**
- Email: admin@admin.com
- Mật khẩu: Vnr@1234

## 🏃‍♂️ Chạy ứng dụng test chatbot

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
|   ├── prompt/             # Các prompt hướng dẫn AI
│   └── main.py             # Entry point
├── docker-compose.yml      # Cấu hình Docker
├── Dockerfile              # Định nghĩa Docker image
└── requirements.txt        # Thư viện phụ thuộc
```

## 🔍 Debug

Để debug ứng dụng trong Docker:
1. Ứng dụng có cấu hình sẵn debugpy port 5678
2. Kết nối với debugger thông qua VS Code


## Test

### Chạy test API

Hệ thống sử dụng pytest để chạy các test tự động kiểm tra tính đúng đắn của API endpoints.

#### Sử dụng Docker (Khuyên dùng)

```bash
# Chạy tất cả test API
make test

# Kiểm tra độ bao phủ code của test
make test-cov
```

#### Không dùng Docker

```bash
# Chạy tất cả test API
pytest -v

# Kiểm tra độ bao phủ code của test
pytest --cov=src tests/ --cov-report term-missing
```

### Test API bằng công cụ

Bạn cũng có thể sử dụng công cụ như Postman, cURL hoặc Swagger UI để test API:

- **Swagger UI**: Truy cập `http://localhost:8000/docs` trong chế độ dev
- **ReDoc**: Truy cập `http://localhost:8000/redoc` trong chế độ dev
- **OpenAPI Spec**: Truy cập `http://localhost:8000/openapi.json` trong chế độ dev