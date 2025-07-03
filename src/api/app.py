from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from .routers.chat import router as chat_router
from .routers.health import router as health_router
from .routers.generate import router as generate_router
from langfuse import Langfuse
from src.config import settings

# Cấu hình logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

Langfuse(
    public_key=settings.LANGFUSE_CONFIG["public_key"],
    secret_key=settings.LANGFUSE_CONFIG["secret_key"],
    host=settings.LANGFUSE_CONFIG["host"],
)

app = FastAPI(
    title="AI API",
    description="API cho ứng dụng AI",
    version="0.1.0"
)

# Cấu hình CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Trong môi trường production, hãy chỉ định các nguồn gốc cụ thể
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Import các router
app.include_router(chat_router)
app.include_router(generate_router)
app.include_router(health_router)