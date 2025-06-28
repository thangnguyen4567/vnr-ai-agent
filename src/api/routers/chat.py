from fastapi import APIRouter, HTTPException, status
from typing import Any, Dict

from ..models.chat_model import AIRequest, AIResponse
from ..services.chat_service import chat_service

# Tạo router
router = APIRouter(
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)

@router.post("/process", response_model=AIResponse)
async def process_ai_request(request: AIRequest) -> Dict[str, Any]:
    """
    Xử lý yêu cầu AI
    
    - **prompt**: Câu hỏi hoặc nhiệm vụ cho AI
    - **context**: Ngữ cảnh bổ sung (tùy chọn)
    - **model_params**: Tham số tùy chỉnh (tùy chọn)
    """
    try:
        response = await chat_service.process_request(
            prompt=request.prompt,
            context=request.context,
            model_params=request.model_params
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi xử lý yêu cầu AI: {str(e)}"
        ) 