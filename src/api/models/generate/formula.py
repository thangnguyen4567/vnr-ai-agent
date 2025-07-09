from pydantic import BaseModel, Field
    
class ChatHistory(BaseModel):
    human: str = Field(description="Nội dung người dùng")
    bot: str = Field(description="Nội dung bot")

class FormulaInput(BaseModel):
    question: str = Field(description="Câu hỏi")
    enum: str = Field(description="Danh sách enum")
    prompt: str = Field(description="Ngữ cảnh")
    chat_history: list[ChatHistory] = Field(description="Lịch sử chat")
    
class FormulaDetail(BaseModel):
    formula: str = Field(
        description="""
        VD: [Tổng doanh số] / [Mục tiêu công ty] * 0.5 (chỉ được quyền sử dụng các enum trong danh sách enum) 
        Sử dụng các công thức và toán tử của excel để thiết lập (Ex: SUM(), IF(), .....) 
        """
    )
    description: str = Field(description="Giải thích công thức")