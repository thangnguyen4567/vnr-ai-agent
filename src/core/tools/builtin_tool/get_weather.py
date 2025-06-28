from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

@tool("get_weather",return_direct=False)
def get_weather(config: RunnableConfig) -> str:
    """Lấy thông tin thời tiết của một thành phố"""
    return f"Thời tiết của thành phố Hà Nội là nắng"