from pydantic import BaseModel, Field
from typing import Literal
from uuid import UUID
from typing import Optional

class GoalInput(BaseModel):
    question: str = Field(description="Câu hỏi")

class GoalDetail(BaseModel):
    ID: UUID = Field(description="ID mục tiêu")
    GoalName: str = Field(description="Tên mục tiêu")
    Department: str = Field(description="Phòng ban")
    TotalTarget: int = Field(description="Tổng mục tiêu")
    MeasurementUnit: str = Field(description="Đơn vị đo lường")
    MeasurementScale: str = Field(description="Loại hướng mục tiêu tăng hoặc giảm")
    ParentID: Optional[UUID] = Field(
        default=None,
        description="ID mục tiêu cha (GUID), nếu không có thì null"
    )
    HasChildren: bool = Field(description="Có con không nếu ko có thì mặc định false")
    Weight: str = Field(description="Trọng số mục tiêu tổng Tổng trọng số mục tiêu tổng là 100%")
    StartDate: str = Field(description="Ngày bắt đầu theo định dạng dd/mm/yyyy")
    EndDate: str = Field(description="Ngày kết thúc theo định dạng dd/mm/yyyy")
    Type: str = Field(description="Phương pháp đo lường mục tiêu")