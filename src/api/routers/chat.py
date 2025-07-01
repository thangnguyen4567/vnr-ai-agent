from fastapi import APIRouter
from typing import Any, Dict
from fastapi.encoders import jsonable_encoder
from ..models.chat_model import PayloadRequest
from ..services.chat_service import ChatService
from sse_starlette.sse import EventSourceResponse
from src.core.config_loader import agent_config_loader
from src.config import settings

# Tạo router
router = APIRouter(
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)


@router.post("/process")
async def dispatch(request_body: PayloadRequest) -> Dict[str, Any]:
    """
    Xử lý yêu cầu AI

    - **input**: Câu hỏi hoặc nhiệm vụ cho AI
    - **config**: Cấu hình cho AI
    """
    input = jsonable_encoder(request_body.input)
    config = jsonable_encoder(request_body.config)

    # Thiết lập loại agent dựa trên config đầu vào
    agent_type = config.get("agent_type", "multi")
    agent_config_loader.set_agent_type("single" if agent_type == "fc" else agent_type)

    # Cấu hình Langfuse từ global_config
    langfuse_handler = ChatService.get_langfuse_handler()

    # Bổ sung cấu hình
    config["callbacks"] = [langfuse_handler] if langfuse_handler else []
    config["recursion_limit"] = 15
    config["metadata"] = {
        "langfuse_user_id": config.get("user_id", "anonymous"),
    }

    return EventSourceResponse(
        ChatService.agent_stream_response(input=input, config=config)
    )
