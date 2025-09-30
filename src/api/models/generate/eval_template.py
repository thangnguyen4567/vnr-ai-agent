from pydantic import BaseModel, Field, create_model
from typing import Optional

class ChatHistory(BaseModel):
    human: Optional[str] = Field(default=None, description="Nội dung người dùng")
    bot: Optional[str] = Field(default=None, description="Nội dung bot")

class EvalTemplateInput(BaseModel):
    template_name: Optional[str] = Field(default=None, description="Tên mẫu đánh giá")
    template_type: Optional[str] = Field(default=None, description="Loại đánh giá")
    departments: Optional[list[str]] = Field(default=None, description="Phòng ban")
    positions: Optional[list[str]] = Field(default=None, description="Vị trí")
    prompt: str = Field(description="Yêu cầu")
    attachment_url: Optional[str] = Field(default=None, description="Url file đính kèm")
    chat_history: Optional[list[ChatHistory]] = Field(default=None, description="Lịch sử chat")
    is_use_system_data: Optional[bool] = Field(default=False, description="Sử dụng dữ liệu hệ thống")
    columns: Optional[list[str]] = Field(default=None, description="Cột động")
    project_code: Optional[str] = Field(default="default", description="Mã dự án")

class EvalTemplateDetail(BaseModel):
    GroupName: str = Field(description="Tên nhóm")
    Id: str = Field(description="ID tiêu chí")
    Code: str = Field(description="Mã tiêu chí")
    Description: str = Field(description="Mô tả tiêu chí năng lực")
    Name: str = Field(description="Tên tiêu chí")
    Weight: int = Field(description="Trọng số")
    GroupId: str = Field(description="ID nhóm")
    DateCreate: str = Field(description="Ngày tạo")
    GroupWeight: int = Field(description="Trọng số nhóm")
    ScoreSettingId: str = Field(description="ID thang điểm")
    checked: bool = Field(description="Đã chọn")

class EvalTemplate(BaseModel):
    data: list[EvalTemplateDetail] = Field(description="Danh sách các tiêu chí năng lực")


def get_eval_template_model(extra_fields: dict = None):
    fields = {
        "GroupName": (str, Field(description="Tên nhóm")),
        "Id": (str, Field(description="ID tiêu chí")),
        "Code": (str, Field(description="Mã tiêu chí")),
        "Description": (str, Field(description="Mô tả tiêu chí năng lực")),
        "Name": (str, Field(description="Tên tiêu chí")),
        "Weight": (int, Field(description="Trọng số")),
        "GroupId": (str, Field(description="ID nhóm")),
        "DateCreate": (str, Field(description="Ngày tạo")),
        "GroupWeight": (int, Field(description="Trọng số nhóm")),
        "ScoreSettingId": (str, Field(description="ID thang điểm")),
        "checked": (bool, Field(description="Đã chọn")),
    }
    if extra_fields:
        fields.update(extra_fields)

    DynamicEvalTemplateDetail = create_model("DynamicEvalTemplateDetail", **fields)
    EvalTemplate = create_model(
        "EvalTemplate",
        data=(list[DynamicEvalTemplateDetail], Field(description="Danh sách các tiêu chí năng lực"))
    )
    return EvalTemplate