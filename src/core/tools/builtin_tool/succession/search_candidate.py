from langchain_core.tools import tool
from src.vectordb.vectordb import VectorDBManager
from redisvl.query.filter import Text

CANDIDATE_DESC_TEMPLATE = "{content} - {metadata}" # content: nội dung của schema, metadata: metadata của schema

@tool("search_candidate",return_direct=False)
async def search_candidate(search_query: str) -> str:
    """
    Tìm kiếm thông tin các ứng viên 
    Args:
        search_query: Từ khóa tìm kiếm
    Returns:
        Thông tin các ứng viên
    """

    vector_db = VectorDBManager()
    filter_condition = Text("type") == "candidate"
    candidates = vector_db.get_documents(search_query, k=20, index_name="succession_data", filter=filter_condition)
    candidates_desc = []

    for a in candidates:
        candidates_desc.append(CANDIDATE_DESC_TEMPLATE.format(content=a.page_content, metadata=a.metadata))

    return '\n'.join(candidates_desc)
  