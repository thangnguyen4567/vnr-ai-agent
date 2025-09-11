from src.vectordb.provider.base import VectorDB
from langchain_redis import RedisConfig, RedisVectorStore
from redis import Redis

class RedisVectorDB(VectorDB):
    def __init__(self):
        super().__init__()
        self.redis_url = self.name + '://' + self.host + ':' + str(self.port)

    def connect_vectordb(self, index_name, index_schema=None):
        """Kết nối đến Redis vector database"""

        # Mẫu schema của redis , cần thiết nếu muốn sử dụng filter
        # index_schema = {
        #     {"name": "category", "type": "tag"},
        #     {"name": "author", "type": "text"},
        #     {"name": "year", "type": "number"},
        #     {"name": "published", "type": "boolean"},
        # }

        config = RedisConfig(
            index_name=index_name,
            redis_url=self.redis_url,
            metadata_schema=index_schema,
        )
 
        vector_store = RedisVectorStore(self.embeddings, config=config)
        return vector_store

    def add_vectordb(self, documents, index_name, index_schema=None):
        """Thêm documents vào Redis vector database"""
        vector_store = self.connect_vectordb(index_name, index_schema)
        vector_store.add_documents(documents)
    
    def similarity_search(self, query, k=2, filter=None, index_name=None, index_schema=None):
        """Tìm kiếm các documents tương tự từ Redis vector database"""
        # Kết nối đến database
        vector_db = self.connect_vectordb(index_name, index_schema)
        # Thực hiện tìm kiếm
        results = vector_db.similarity_search(
            query, 
            k=k,
            filter=filter
        )
        
        return results

    def delete_index(self, index_name):
        """Xóa index trong Redis vector database"""
        r = Redis(host=self.host, port=self.port, decode_responses=True)
        # Xóa index + tất cả key/doc trong đó
        try:
            r.ft(index_name).dropindex(delete_documents=True)
            print(f"✅ Đã xóa thành công index: {index_name}")
        except Exception as e:
            print(f"❌ Lỗi khi xóa index {index_name}: {e}")
    