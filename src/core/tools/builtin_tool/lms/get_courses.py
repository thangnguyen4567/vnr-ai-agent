from langchain_core.tools import tool
from langchain_core.runnables import RunnableConfig
from src.vectordb.vectordb import VectorDBManager
import re

@tool("get_courses",return_direct=False)
def get_courses(search: str, config: RunnableConfig = None) -> str:
    """Lấy danh sách khóa học, tóm tắt khóa học, tìm kiếm khóa học"""
    collection = 'course_LMS_DEMO5'

    index_schema = {
        "text": [
            {"name":"source"},
            {"name":"title"},
            {"name":"content"},
        ],
        "numeric": [
            {"name":"courseid"},
        ]
    }
    try:
        vector_db = VectorDBManager()

        documents = vector_db.get_documents(search, k=6, index_name=collection, index_schema=index_schema)

        result = ''
        for doc in documents:
            result += re.sub(r"[{}]", "", doc.page_content)
            result += 'Link khóa học:' + doc.metadata['source'] + '--Hết thông tin khóa học--.\n'
        return result

    except Exception as e:
        return str(e)
