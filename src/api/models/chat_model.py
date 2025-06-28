from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any


class AIRequest(BaseModel):
    """Mô hình yêu cầu AI"""
    prompt: str = Field(..., description="Câu hỏi hoặc nhiệm vụ cho AI")
    context: Optional[str] = Field(None, description="Ngữ cảnh bổ sung cho câu hỏi")
    model_params: Optional[Dict[str, Any]] = Field(None, description="Tham số tùy chỉnh cho mô hình")


class AIResponse(BaseModel):
    """Mô hình phản hồi từ AI"""
    response: str = Field(..., description="Phản hồi từ AI")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Metadata của phản hồi")
    status: str = Field("success", description="Trạng thái của phản hồi") 