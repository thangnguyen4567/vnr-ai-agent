from dis import Positions
from langchain_core.tools import tool
from src.vectordb.vectordb import VectorDBManager
from redisvl.query.filter import Text

POSITION_DESC_TEMPLATE = "{content} - {metadata}" # content: nội dung của schema, metadata: metadata của schema

@tool("search_position",return_direct=False)
async def search_position(search_query: str) -> str:
    """
    Tìm kiếm thông tin các vị trí cần người kế nhiệm
    Args:
        search_query: Từ khóa tìm kiếm
    Returns:
        Thông tin các vị trí cần người kế nhiệm
    """

    vector_db = VectorDBManager()
    filter_condition = Text("type") == "position"
    positions = vector_db.get_documents(search_query, k=20, index_name="succession_data", filter=filter_condition)
    positions_desc = []

    for a in positions:
        positions_desc.append(POSITION_DESC_TEMPLATE.format(content=a.page_content, metadata=a.metadata))

    return '\n'.join(positions_desc)
  