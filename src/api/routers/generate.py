from fastapi import APIRouter
from typing import Any, Dict
from ..models.chat_model import PayloadRequest

# Tạo router
router = APIRouter(
    prefix="/generate",
    tags=["Generate"],
    responses={404: {"description": "Not found"}},
)

@router.post("/goal")
async def create_goal(request_body: PayloadRequest) -> Dict[str, Any]:
    return {"message": "Hello, World!"}


@router.post("/formula")
async def create_formula(request_body: PayloadRequest) -> Dict[str, Any]:
    return {"message": "Hello, World!"}


