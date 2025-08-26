from src.vectordb.provider.base import VectorDB
from langchain_redis import RedisConfig, RedisVectorStore

class RedisVectorDB(VectorDB):
    def __init__(self):
        super().__init__()
        self.redis_url = self.name + '://' + self.host + ':' + str(self.port)

    def connect_vectordb(self, index_name, index_schema=None):
        """Kết nối đến Redis vector database"""
        config = RedisConfig(
            index_name=index_name,
            redis_url=self.redis_url,
            metadata_schema=index_schema
        )
        vector_store = RedisVectorStore(self.embeddings, config=config)
        return vector_store

    def add_vectordb(self, documents, index_name, index_schema=None):
        """Thêm documents vào Redis vector database"""
        vector_store = self.connect_vectordb(index_name, index_schema)
        vector_store.add_documents(documents)
    
    def similarity_search(self, query, k=2, filter=None, index_name=None):
        """Tìm kiếm các documents tương tự từ Redis vector database"""
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
