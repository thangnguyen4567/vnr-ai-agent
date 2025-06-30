from pydantic import BaseModel, Field
from typing import List, Literal, Union, Dict, Any
from datetime import datetime


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

    # def __init__(self, **data):
    #     content = data.get("content")
    #     if isinstance(content, str):
    #         data["content"] = TextContent(type="text", text=content)
    #     super().__init__(**data)


class InputData(BaseModel):
    messages: List[Message] = Field(default_factory=list)


class Config(BaseModel):
    user_id: str = Field("113", description="ID người dùng")
    user_name: str = Field("Thang", description="Tên người dùng")
    current_date: str = Field(
        datetime.now().strftime("%d/%m/%Y"), description="Ngày hiện tại"
    )
    language: str = Field("vi-VN", description="Ngôn ngữ")
    agent_id: str = Field(..., description="ID agent")
    recursion_limit: int = Field(10, description="Giới hạn đệ quy")
    agent_type: Literal["multi", "fc"] = Field("multi", description="Loại agent")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Metadata")


class PayloadRequest(BaseModel):
    input: InputData = Field(..., description="Dữ liệu đầu vào")
    config: Config = Field(..., description="Cấu hình")
