from langchain_community.vectorstores import Redis
from src.vectordb.provider.base import VectorDB

class RedisVectorDB(VectorDB):
    def __init__(self):
        super().__init__()
        self.redis_url = self.name + '://' + self.host + ':' + str(self.port)

    def connect_vectordb(self, index_name, index_schema=None):
        """Kết nối đến Redis vector database"""
        vector_db = Redis.from_existing_index(
            self.embeddings,
            index_name=index_name,
            redis_url=self.redis_url,
            schema=index_schema
        )
        return vector_db

    def add_vectordb(self, documents, index_name):
        """Thêm documents vào Redis vector database"""
        Redis.from_documents(
            documents=documents,
            embedding=self.embeddings,
            index_name=index_name,
            redis_url=self.redis_url
        )
    
    def similarity_search(self, query, k=2, filter=None):
        """Tìm kiếm các documents tương tự từ Redis vector database"""
        # Sử dụng index mặc định nếu không được chỉ định
        index_name = "my_documents"
        
        # Kết nối đến database
        vector_db = self.connect_vectordb(index_name)
        
        # Redis sử dụng filter theo cách khác, cần chuyển đổi format filter
        redis_filter = None
        if filter and isinstance(filter, list):
            redis_filter = {"metadata.source": {"$in": filter}}
            
        # Thực hiện tìm kiếm
        results = vector_db.similarity_search(
            query, 
            k=k,
            filter=redis_filter
        )
        
        return results
