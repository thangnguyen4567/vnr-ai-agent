from pydantic import BaseModel, Field

class GoalInput(BaseModel):
    question: str = Field(description="Câu hỏi")

class GoalDetail(BaseModel):
    ID: int = Field(description="ID mục tiêu")
    GoalName: str = Field(description="Tên mục tiêu")
    Department: str = Field(description="Phòng ban")
    TotalTarget: int = Field(description="Tổng mục tiêu")
    Unit: str = Field(
        description="Đơn vị ('currency' : tiền, 'percent' : phần trăm, 'number' : số lượng)"
    )
    ParentID: int = Field(description="ID mục tiêu cha nếu ko có thì mặc định null")
    HasChildren: bool = Field(description="Có con không nếu ko có thì mặc định false")
    Weight: str = Field(
        description="Trọng số mục tiêu tổng Tổng trọng số mục tiêu tổng là 100%"
    )
    Type: str = Field(
        description="Loại mục tiêu 'Tài chính', 'Khách hàng', 'Nội bộ', 'Sản phẩm', 'Quy trình', 'Khác', 'Đào tạo & Phát triển'"
    )
    # Guideline: str = Field(description="Hướng dẫn thực hiện mục tiêu")