from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from src.vectordb.vectordb import VectorDBManager
import re

@tool("get_hdsd",return_direct=False)
def get_hdsd(search: str, config: RunnableConfig = None) -> str:
    """Lấy danh sách tài liệu hướng dẫn sử dụng hệ thống elearning VD: cách tạo khóa học, cách tạo bài giảng, 
    cách tạo tài liệu, gamification, lộ trình, câu hỏi, đánh giá..."""

    index_schema = {
        "text": [
            {"name":"title"},
            {"name":"role"},
            {"name":"content"},
            {"name":"source"}
        ],
    }

    try:
        documents = VectorDBManager().connect_vectordb(collection_name='system',index_schema=index_schema).similarity_search(search,k=8)
        result = ''
        for doc in documents:
            result += re.sub(r"[{}]", "", doc.page_content)
            result += ' Link tài liệu hdsd: ['+doc.metadata['title']+']' + (doc.metadata['source'] if doc.metadata['source'] != None else '') + '.\n'
        return result

    except Exception as e:
        return str(e)
