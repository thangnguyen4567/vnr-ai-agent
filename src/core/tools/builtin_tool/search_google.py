from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig

@tool("search_google", return_direct=False)
def search_google(config: RunnableConfig) -> str:
    """Tìm kiếm nhanh trên Google (demo đơn giản, không dùng API thật)."""
    return f"Có một con chó tên là Mèo"