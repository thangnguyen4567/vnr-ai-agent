from fastapi import APIRouter, status
from typing import Dict
import time
import psutil
import platform

# Tạo router
router = APIRouter(
    tags=["Health"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", status_code=status.HTTP_200_OK)
async def health_check() -> Dict:
    """
    Kiểm tra trạng thái API

    Trả về:
    - **status**: Trạng thái hoạt động của API
    - **timestamp**: Thời gian kiểm tra
    """
    return {"status": "healthy", "timestamp": time.time()}


@router.get("/details", status_code=status.HTTP_200_OK)
async def health_details() -> Dict:
    """
    Chi tiết về trạng thái hệ thống

    Trả về:
    - **status**: Trạng thái hoạt động của API
    - **system_info**: Thông tin hệ thống
    - **resources**: Thông tin về tài nguyên hệ thống
    - **timestamp**: Thời gian kiểm tra
    """
    try:
        memory = psutil.virtual_memory()
        disk = psutil.disk_usage("/")

        return {
            "status": "healthy",
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
                "machine": platform.machine(),
            },
            "resources": {
                "cpu_usage": psutil.cpu_percent(interval=0.1),
                "memory": {
                    "total_gb": round(memory.total / (1024**3), 2),
                    "available_gb": round(memory.available / (1024**3), 2),
                    "usage_percent": memory.percent,
                },
                "disk": {
                    "total_gb": round(disk.total / (1024**3), 2),
                    "free_gb": round(disk.free / (1024**3), 2),
                    "usage_percent": disk.percent,
                },
            },
            "timestamp": time.time(),
        }
    except Exception as e:
        # Nếu không có quyền truy cập vào thông tin hệ thống, trả về thông tin cơ bản
        return {
            "status": "healthy",
            "system_info": {
                "platform": platform.platform(),
                "python_version": platform.python_version(),
            },
            "error": str(e),
            "timestamp": time.time(),
        }
