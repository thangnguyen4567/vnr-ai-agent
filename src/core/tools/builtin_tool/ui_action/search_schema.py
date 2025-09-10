from langchain_core.tools import tool
from src.vectordb.vectordb import VectorDBManager
from typing import Literal
from src.prompt import SCREEN_DESC_TEMPLATE

@tool("search_schema",return_direct=False)
async def search_schema(screen_name: str, type_screen: Literal['human-resources', 'objEval']) -> str:
    """
    Tìm kiếm schema màn hình để AI có thể thực hiện hành động trên màn hình đó. Luôn phải thực hiện tìm kiếm search_schema trước khi thực hiện các action.
    Args:
        screen_name: Tên màn hình
        module: màn hình thuộc module phân hệ nào (objEval: phân hệ đánh giá , mục tiêu, human-resources: phân hệ nhân sự)
    Returns:
        Schema các màn hình tìm được
    """

    vector_db = VectorDBManager()
    screen_schema = vector_db.get_documents(screen_name, k=6, index_name="ui_schema")
    screen_desc = []

    for a in screen_schema:
        if type_screen in a.metadata["pageId"]:
            screen_desc.append(SCREEN_DESC_TEMPLATE.format(pageId=a.metadata["pageId"], schema=a))

    return '\n'.join(screen_desc)