from fastapi import APIRouter
from typing import Any, Dict
from src.api.services.generate_service import GenerateService
from src.api.models.generate.goal import GoalInput
from src.api.models.generate.formula import FormulaInput
from fastapi import HTTPException

# Tạo router
router = APIRouter(
    prefix="/generate",
    tags=["Generate"],
    responses={404: {"description": "Not found"}},
)

@router.post("/goal")
async def create_goal(input: GoalInput) -> Dict[str, Any]:
    try:
        return GenerateService().create_goal(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/formula")
async def create_formula(input: FormulaInput) -> Dict[str, Any]:
    try:
        return GenerateService().create_formula(input)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


