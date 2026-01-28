# VNR AI Agent Platform

## 🤖 Giới thiệu

Nền tảng xây dựng và vận hành AI Agent với LangGraph và LangChain, giúp phát triển và triển khai các hệ thống AI thông minh.

### Kiến trúc Multi-agent supervisor

<img src="https://langchain-ai.github.io/langgraph/tutorials/multi_agent/assets/diagram.png" alt="Kiến trúc Multi-agent supervisor" width="500"/>

Tham khảo: https://langchain-ai.github.io/langgraph/tutorials/multi_agent/agent_supervisor/

### VectorDB

VNR AI Agent Platform sử dụng Qdrant làm Vector Database để lưu trữ và truy vấn các vector embeddings, giúp agent có thể tìm kiếm thông tin liên quan dựa trên ngữ nghĩa.

#### Cách hoạt động

1. **Embedding Generation**: Dữ liệu văn bản được chuyển đổi thành vector embeddings thông qua các mô hình như OpenAI Ada, BERT hoặc các mô hình tương tự.
2. **Vector Storage**: Các vector được lưu trữ trong Qdrant cùng với metadata để dễ dàng truy xuất.
3. **Semantic Search**: Khi cần tìm kiếm thông tin, câu truy vấn được chuyển đổi thành vector và so sánh với các vector trong cơ sở dữ liệu để tìm ra kết quả có độ tương đồng cao nhất.

#### Sử dụng trong Multi-Agent

Agent sử dụng VectorDB để:

- **Truy xuất kiến thức**: Tìm kiếm thông tin từ kho dữ liệu lớn
- **Ghi nhớ hội thoại**: Lưu trữ và truy vấn các phiên trò chuyện trước đó
- **Context Augmentation**: Bổ sung ngữ cảnh để agent đưa ra quyết định chính xác hơn

#### Cài đặt và sử dụng

- Đã được cấu hình trong `docker-compose.yml`, chỉ cần chạy `docker-compose up -d`
- Truy cập dashboard Qdrant tại: http://localhost:6333/dashboard

## 🚀 Tính năng chính

- **Multi-Agent Framework**: Xây dựng hệ thống đa agent với LangGraph
- **Giao diện Streamlit**: Tương tác trực quan với agent qua giao diện chat
- **API FastAPI**: Tích hợp agent vào các ứng dụng thông qua RESTful API
- **Giám sát với Langfuse**: Theo dõi và phân tích hiệu suất agent trong thời gian thực
- **Lưu trữ trạng thái**: Hỗ trợ checkpointing

## 🔧 Cài đặt

### Yêu cầu

- Python 3.11+ (khuyên dùng Python 3.13)
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
# Khởi chạy toàn bộ hệ thống (bao gồm vectorDB và Langfuse)
docker-compose up -d

# Chỉ khởi chạy dịch vụ AI Agent
docker-compose up agent-api -d
```

## ⚙️ Cấu hình

Hệ thống cấu hình của VNR AI Agent Platform được quản lý thông qua các file YAML trong thư mục `settings/`:

- **settings/llm.yaml**: Cấu hình cho các mô hình ngôn ngữ lớn (LLM)
- **settings/multi_agent.yaml**: Định nghĩa cấu trúc và thuộc tính của hệ thống đa agent
- **settings/fc_agent.yaml**: Cấu hình cho function-calling agent
- **settings/langfuse.yaml**: Cấu hình cho hệ thống giám sát Langfuse

Các file cấu hình được tải tự động khi khởi động ứng dụng bởi `ConfigReaderInstance` trong module `src.utils`. Người dùng có thể chỉnh sửa các file này để thay đổi hành vi của hệ thống AI Agent.

Để thêm mới hoặc cập nhật cấu hình:

1. Chỉnh sửa file cấu hình tương ứng trong thư mục `settings/`
2. Khởi động lại ứng dụng để áp dụng các thay đổi

### Cấu trúc file multi_agent.yaml

File `multi_agent.yaml` định nghĩa hệ thống đa agent với cấu trúc chi tiết như sau:

#### Thông tin cơ bản

```yaml
agent_id: "d4e12d5bb4014794fa3f956e2b0e01cf" # ID duy nhất của multi agent
name: "Multi Agent" # Tên hiển thị
type: "multi" # Loại agent (multi/fc)
```

#### Danh sách Agents

Mỗi agent được định nghĩa với ID riêng và mô tả chức năng:

```yaml
agents:
  - id: "f4e9a767bf49f68a77f7afd783665df9" # ID duy nhất cho mỗi agent
    name: "Goal Agent" # Tên hiển thị
    description: "Agent tìm kiếm thông tin về mục tiêu KPI của phòng ban bộ phận" # Cần mô tả kỹ để AI phân tích chọn Agent phù hợp
```

#### Cấu hình Sub-agents

Mỗi sub-agent được định nghĩa chi tiết với:

```yaml
sub_agents:
  - agent_id: "f4e9a767bf49f68a77f7afd783665df9" # ID tham chiếu đến agent trong danh sách
    name: "Goal Agent" # Tên hiển thị
    type: "fc" # Loại agent (fc = function calling)
    nodes:
      llm: # Cấu hình LLM cho agent này
        model: "gpt-4o-mini" # Mô hình LLM sử dụng
        temperature: 0.5 # Độ sáng tạo (0-1)
        max_tokens: 1000 # Giới hạn token đầu ra
        provider: "openai" # Nhà cung cấp LLM
        agent_prompt: "" # Prompt đặc biệt cho agent
```

#### Định nghĩa Tools

Mỗi agent có thể có nhiều tools, được chia làm 2 loại chính:

##### 1. Built-in Tools

Tools được định nghĩa sẵn trong code của hệ thống:

```yaml
tools:
  - type: built_in # Loại tool: built_in
    name: get_goal # Tên của tool
    description: "Lấy danh sách mục tiêu KPI của phòng ban bộ phận" # Mô tả
```

##### 2. HTTP Tools (API động)

Tools kết nối đến API bên ngoài:

```yaml
tools:
  - type: http # Loại tool: http
    name: get_weather # Tên của tool
    method: POST # Phương thức mặc định là get
    description: "Lấy thông tin thời tiết của thành phố"
    tool_path: https://api.open-meteo.com/v1/forecast # Endpoint API

    # Các tham số đầu vào
    input_params:
      - name: latitude # Tên tham số
        description: "Vĩ độ" # Mô tả
        input_method: query # Phương thức truyền: query, header, path, body
        type: number # Kiểu dữ liệu
        default: 21.03 # Giá trị mặc định

      - name: x-api-key # Ví dụ về tham số header
        description: "API key"
        input_method: header # Phương thức truyền: header
        type: string
        default: reqres-free-v1

    # Định nghĩa output
    output_params:
      - name: current_weather # Tên trường dữ liệu trả về
        type: string # Kiểu dữ liệu
        description: "Thời tiết hiện tại" # Mô tả
```

##### 3. Dynamic Store Tools

Tools lấy dữ liệu từ hệ thống lưu trữ (dynamic store):

```yaml
- type: store # Xác định loại tool là store
  name: get_progress_overview # Tên của công cụ
  description: "Lấy danh sách tiến độ mục tiêu" # Mô tả chức năng
  tool_path: sp_eva_get_progress_overview # Đường dẫn API
  input_params: [] # Các tham số đầu vào (nếu có)
  method: GET # Phương thức HTTP
  store_name: sp_eva_get_progress_overview # Tên của store
  tool_type: dynamic # Loại tool là dynamic hoặc standard
```

##### 4. Workflow Tools

Tools thực hiện các quy trình nghiệp vụ phức tạp:

```yaml
- type: workflow # Xác định loại tool là workflow
  name: register_goal # Tên của workflow
  description: "Thực hiện giao mục tiêu cho phòng ban bộ phận hoặc cá nhân"
  input_params: # Danh sách các tham số đầu vào
    - name: type # Tên của tham số
      description: "loại mục tiêu có thể là 1 trong KPI, OKR, SMART"
      input_method: query # Phương thức truyền tham số
      type: string # Kiểu dữ liệu
      default: KPI # Giá trị mặc định
      required: true # Tham số bắt buộc hay không
    # Các tham số khác...
  token_workflow: app-6c94IEkTQ0sO4WxkTTiCkOFp # Mã token xác thực workflow
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
- **array**: Dữ liệu dạng mảng
- **object**: Dữ liệu dạng object

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

## Trực quan hóa

### Hiển thị workflow của Multi-agent bằng Mermaid

Multi-agent workflow có thể được trực quan hóa dưới dạng biểu đồ Mermaid, giúp dễ dàng hiểu được cấu trúc và luồng hoạt động của hệ thống.

#### Sử dụng script graph.py

Chúng tôi cung cấp script `graph.py` để chuyển đổi file cấu hình YAML thành biểu đồ Mermaid:

```bash
python graph.py
```

#### Hiển thị với Mermaid Live Editor

1. Truy cập [https://mermaid.live/](https://mermaid.live/)
2. Sao chép nội dung từ cmd
3. Dán vào khung soạn thảo bên trái của Mermaid Live Editor
4. Biểu đồ sẽ được hiển thị ở khung bên phải

Trực quan hóa giúp người dùng và nhà phát triển dễ dàng hiểu cấu trúc phức tạp của hệ thống Multi-agent.
