from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .routers.chat import router as chat_router
from .routers.health import router as health_router
from .routers.generate import router as generate_router
from langfuse import Langfuse
from src.config import settings
from src.vectordb.vectordb import VectorDBManager
import os
# Cấu hình logging

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="logs/dev.log",        # 👈 Ghi log vào file app.log
    filemode="a"               # "a" để ghi tiếp, "w" để ghi đè
)

# Khởi tạo VectorDBManager
VectorDBManager()

app = FastAPI(
    title="AI Agent API",
    description="API cho ứng dụng AI Agent",
    version="0.1.0",
    docs_url='/docs' if settings.DEV_MODE else None,
    redoc_url='/redoc' if settings.DEV_MODE else None,
    openapi_url='/openapi.json' if settings.DEV_MODE else None,
)

origins = [
    "http://localhost:4200", # Test localhost
    "https://demo33.vnresource.net:3339", # Test demo33
    "https://qc-core.vnrlocal.com:3019", # Test qc-core
    "https://qc-core.vnrlocal.com:3009", # Test qc-core
    "http://127.0.0.1:8000", # Test localhost
]

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Trong môi trường production, hãy chỉ định các nguồn gốc cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Import các router
app.include_router(chat_router)
app.include_router(generate_router)
app.include_router(health_router)