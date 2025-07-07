from fastapi import APIRouter
from typing import Any, Dict

# Tạo router
router = APIRouter(
    prefix="/generate",
    tags=["Generate"],
    responses={404: {"description": "Not found"}},
)

@router.post("/goal")
async def create_goal() -> Dict[str, Any]:
    return {"message": "Hello, World!"}


@router.post("/formula")
async def create_formula() -> Dict[str, Any]:
    return {"message": "Hello, World!"}


