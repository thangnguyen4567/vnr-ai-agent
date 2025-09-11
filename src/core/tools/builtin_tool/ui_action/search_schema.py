from langchain_core.tools import tool
from src.vectordb.vectordb import VectorDBManager
from typing import Literal
from redisvl.query.filter import Text

SCREEN_DESC_TEMPLATE = "{content} - {metadata}" # content: nội dung của schema, metadata: metadata của schema

@tool("search_screen_schema",return_direct=False)
async def search_screen_schema(screen_name: str, type_screen: Literal['human-resources', 'objEval']) -> str:
    """
    Tìm kiếm schema màn hình để AI có thể thực hiện hành động trên màn hình đó. Luôn phải thực hiện tìm kiếm search_schema trước khi thực hiện các action.
    Args:
        screen_name: Tên màn hình cần tìm kiếm ( ví dụ: nhân sự, đánh giá, mục tiêu, tuyển dụng, ...) Lưu ý luôn truyền vào tiếng việt
        type_screen: màn hình thuộc module phân hệ nào (objEval: phân hệ đánh giá , mục tiêu, human-resources: phân hệ nhân sự)
    Returns:
        Schema các màn hình tìm được
    """

    vector_db = VectorDBManager()
    filter_condition = Text("pageId") == type_screen
    screen_schema = vector_db.get_documents(screen_name, k=8, index_name="ui_schema", filter=filter_condition)
    screen_desc = []

    for a in screen_schema:
        if type_screen in a.metadata["pageId"]:
            # Xóa pageId khỏi metadata
            del a.metadata["pageId"]
            screen_desc.append(SCREEN_DESC_TEMPLATE.format(content=a.page_content, metadata=a.metadata))

    return '\n'.join(screen_desc)