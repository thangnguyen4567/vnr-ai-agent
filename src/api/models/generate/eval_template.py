from pydantic import BaseModel, Field
from typing import Optional

class ChatHistory(BaseModel):
    human: Optional[str] = Field(default=None, description="Nội dung người dùng")
    bot: Optional[str] = Field(default=None, description="Nội dung bot")

class EvalTemplateInput(BaseModel):
    template_name: Optional[str] = Field(default=None, description="Tên mẫu đánh giá")
    template_type: Optional[str] = Field(default=None, description="Loại đánh giá")
    prompt: str = Field(description="Yêu cầu")
    attachment_url: Optional[str] = Field(default=None, description="Url file đính kèm")
    chat_history: Optional[list[ChatHistory]] = Field(default=None, description="Lịch sử chat")


class EvalTemplateDetail(BaseModel):
    GroupName: str = Field(description="Tên nhóm")
    Id: str = Field(description="ID tiêu chí")
    Code: str = Field(description="Mã tiêu chí")
    Name: str = Field(description="Tên tiêu chí")
    Weight: int = Field(description="Trọng số")
    GroupId: str = Field(description="ID nhóm")
    DateCreate: str = Field(description="Ngày tạo")
    GroupWeight: int = Field(description="Trọng số nhóm")
    ScoreSettingId: str = Field(description="ID thang điểm")
    checked: bool = Field(description="Đã chọn")