from pydantic import BaseModel, Field
from typing import List, Literal, Union, Dict, Any

class TextContent(BaseModel):
    type: Literal["text"] = Field(..., description="Loại nội dung")
    text: str = Field(..., description="Nội dung văn bản")

class ImageContent(BaseModel):
    type: Literal["image_url"] = Field(..., description="Loại nội dung")
    image_url: str = Field(..., description="URL hình ảnh")

MessageContent = Union[TextContent, ImageContent]

class Message(BaseModel):
    role: Literal["user", "assistant"] = Field(..., description="Vai trò của tin nhắn")
    content: str = Field(..., description="Nội dung của tin nhắn")

class InputData(BaseModel):
    messages: List[Message] = Field(default_factory=list)

class Configurable(BaseModel):
    thread_id: str = Field(..., description="ID thread")
    agent_id: str = Field("d4e12d5bb4014794fa3f956e2b0e01cf", description="ID agent")
    language: str = Field("vi-VN", description="Ngôn ngữ")
    current_date: str = Field(..., description="Ngày hiện tại")
    user_info: Dict[str, str] = Field(..., description="Thông tin người dùng")

class Config(BaseModel):
    recursion_limit: int = Field(10, description="Giới hạn đệ quy")
    agent_type: Literal["multi", "fc"] = Field("multi", description="Loại agent")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")
    configurable: Configurable = Field(..., description="Cấu hình")

class PayloadRequest(BaseModel):
    input: InputData = Field(..., description="Dữ liệu đầu vào")
    config: Config = Field(..., description="Cấu hình")
