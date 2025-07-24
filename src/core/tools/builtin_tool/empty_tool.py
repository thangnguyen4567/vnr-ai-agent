from langchain_core.tools import tool

@tool("empty_tool",return_direct=False)
def empty_tool() -> str:
    """
    Dùng để trả lời các câu hỏi không liên quan, mà các tool khác không thể trả lời được ( chỉ gọi tool này 1 lần duy nhất ), 
    Nếu không có tool nào phù hợp mặc định dùng tool này, nếu có tool nào phù hợp thì không dùng tool này
    """
    return ""