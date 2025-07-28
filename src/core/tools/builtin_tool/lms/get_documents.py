from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from src.vectordb.vectordb import VectorDBManager
import re

@tool("get_documents",return_direct=False)
def get_documents(search: str, config: RunnableConfig = None) -> str:
    """Lấy danh sách tài liệu trong khóa học, tóm tắt tài liệu , tìm kiếm tài liệu"""
    collection = 'resource_LMS_DEMO5'

    index_schema = {
        "text": [
            {"name":"source"},
            {"name":"title"},
            {"name":"content"},
        ],
        "numeric": [
            {"name":"courseid"},
            {"name":"coursemoduleid"},
        ]
    }
    try:
        documents = VectorDBManager().connect_vectordb(collection_name=collection,index_schema=index_schema).similarity_search(search,k=8)
        result = ''
        for doc in documents:
            result += re.sub(r"[{}]", "", doc.page_content)
            result += 'Nguồn '+ doc.metadata['title'] + ':' + doc.metadata['source'] + '.\n'
        return result

    except Exception as e:
        return str(e)
