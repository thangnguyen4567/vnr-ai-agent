from langchain_core.documents import Document
from src.config import settings

class VectorDBManager:
    """Quản lý việc tạo và sử dụng các provider vector database"""
    
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorDBManager, cls).__new__(cls)
            cls._instance._init_manager()
        return cls._instance

    def _init_manager(self):
        self.provider = None
        self.provider_type = settings.VECTORDB_CONFIG.get("provider", "qdrant")
        self._initialize_provider()
        
    def _initialize_provider(self):
        """Khởi tạo provider dựa trên cấu hình"""
        if self.provider_type == "redis":
            from src.vectordb.provider.redis import RedisVectorDB
            self.provider = RedisVectorDB()
        elif self.provider_type == "qdrant":
            from src.vectordb.provider.qdrant import QdrantVectorDB
            self.provider = QdrantVectorDB()
        else:
            raise ValueError(f"Không hỗ trợ provider: {self.provider_type}")
    
    def add_documents(self, documents: list[Document], collection_name):
        """Thêm documents vào vector database"""
        self.provider.add_vectordb(documents, collection_name)
    
    def connect_vectordb(self, collection_name, index_schema=None):
        """Kết nối đến vector database"""
        return self.provider.connect_vectordb(collection_name, index_schema)
    
    def get_documents(self, query: str, k: int = 2, collection_name: str = None, filter=None):
        """Tìm kiếm documents tương tự với query"""
        import time
        
        # Bắt đầu đo thời gian
        start_time = time.time()
        
        # Thực hiện tìm kiếm
        results = self.provider.similarity_search(query, k=k, collection_name=collection_name, filter=filter)
        
        # Kết thúc đo thời gian và tính toán
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Thời gian tìm kiếm: {execution_time:.4f} giây")
        
        return results
