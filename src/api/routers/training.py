from typing import Any, Dict

from fastapi import APIRouter, HTTPException, Request

from src.api.services.training.training_factory import TrainingFactory

# Tạo router
router = APIRouter(
    prefix="/training",
    tags=["Training"],
    responses={404: {"description": "Not found"}},
)


async def _parse_body(request: Request) -> Dict[str, Any]:
    """Đọc body dạng JSON hoặc form (giữ tương thích với FE cũ).

    Bản Flask cũ ưu tiên ``request.form`` rồi mới tới ``request.get_json()``.
    FE gửi training data dạng JSON (do có object lồng ``contextdata``), nên
    ưu tiên JSON, fallback sang form.
    """
    content_type = request.headers.get("content-type", "")
    if "application/json" in content_type:
        return await request.json()

    form = await request.form()
    if form:
        return dict(form)

    return await request.json()


@router.post("/training")
async def save_training_data(request: Request) -> Dict[str, Any]:
    try:
        data = await _parse_body(request)
        training = TrainingFactory().create_training(data["type"])
        return training.save_training_data(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/delete")
async def delete_training_data(request: Request) -> Dict[str, Any]:
    try:
        data = await _parse_body(request)
        training = TrainingFactory().create_training(data["type"])
        return training.delete_training_data(data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
