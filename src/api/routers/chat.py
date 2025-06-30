from fastapi import APIRouter
from typing import Any, Dict
from fastapi.encoders import jsonable_encoder
from ..models.chat_model import PayloadRequest
from ..services.chat_service import ChatService
from sse_starlette.sse import EventSourceResponse
from src.core.config_loader import agent_config_loader

# Tạo router
router = APIRouter(
    tags=["Chat"],
    responses={404: {"description": "Not found"}},
)


@router.post("/process")
async def dispatch(session_id: str, request_body: PayloadRequest) -> Dict[str, Any]:
    """
    Xử lý yêu cầu AI

    - **input**: Câu hỏi hoặc nhiệm vụ cho AI
    - **config**: Cấu hình cho AI
    """
    input = jsonable_encoder(request_body.input)
    config = jsonable_encoder(request_body.config)

    agent_config_loader.set_agent_type(config["agent_type"])

    langfuse_handler = ChatService.get_langfuse_handler(session_id, config)
    config["callbacks"] = [langfuse_handler]
    config["recursive_limit"] = 15
    config["metadata"] = {
        "langfuse_user_id": config["user_id"],
    }

    return EventSourceResponse(
        ChatService.agent_stream_response(
            input=input, config=config, session_id=session_id
        )
    )
