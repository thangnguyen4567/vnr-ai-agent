from fastapi import APIRouter, HTTPException    
from typing import Any, Dict
from fastapi.encoders import jsonable_encoder
from ..models.chat_model import PayloadRequest, SpeechRequest
from ..services.chat_service import ChatService
from sse_starlette.sse import EventSourceResponse
from src.core.config_loader import agent_config_loader
from fastapi.responses import StreamingResponse
from gtts import gTTS
import io
from pydub import AudioSegment

# Tạo router
router = APIRouter(
    prefix="/chat",
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

    return EventSourceResponse(
        ChatService.agent_stream_response(input=input, config=config)
    )

@router.post("/voice", response_class=StreamingResponse)
async def create_speech(req: SpeechRequest):
    if not req.text:
        raise HTTPException(status_code=400, detail="Không có dữ liệu")

    # Tạo giọng nói từ gTTS
    tts = gTTS(text=req.text, lang=req.lang)
    audio_buffer = io.BytesIO()
    tts.write_to_fp(audio_buffer)

    # Đọc lại file mp3 từ buffer
    audio_buffer.seek(0)
    audio = AudioSegment.from_file(audio_buffer, format="mp3")

    # Tăng tốc độ phát
    playback_speed = 1.1 if req.lang == 'en' else 1.3
    faster_audio = audio.speedup(playback_speed=playback_speed)

    # Ghi ra buffer để trả về
    output_buffer = io.BytesIO()
    faster_audio.export(output_buffer, format="mp3")
    output_buffer.seek(0)

    return StreamingResponse(output_buffer, media_type="audio/mpeg")