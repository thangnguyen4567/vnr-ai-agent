from abc import ABC, abstractmethod
from src.config import settings
from langchain_openai import OpenAIEmbeddings

class VectorDB(ABC):
    """Lớp trừu tượng định nghĩa giao diện chung cho tất cả các provider vector database"""
    
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            api_key=settings.LLM_CONFIG["openai"]["api_key"]
        )
        self.host = settings.VECTORDB_CONFIG["host"]
        self.port = settings.VECTORDB_CONFIG["port"]
        self.name = settings.VECTORDB_CONFIG.get("name", "")
    
    @abstractmethod
    def connect_vectordb(self, index_name, index_schema=None):
        """Kết nối đến vector database với index đã tồn tại"""
        pass
    
    @abstractmethod
    def add_vectordb(self, documents, index_name):
        """Thêm documents vào vector database"""
        pass
    
    @abstractmethod
    def similarity_search(self, query, k=2, filter=None):
        """Tìm kiếm các documents tương tự"""
        pass
