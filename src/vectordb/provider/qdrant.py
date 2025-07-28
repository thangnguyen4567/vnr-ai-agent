from qdrant_client import QdrantClient, models
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from src.vectordb.provider.base import VectorDB

class QdrantVectorDB(VectorDB):
    def __init__(self):
        super().__init__()
        self.client = QdrantClient(
            host=self.host, 
            port=self.port, 
            prefer_grpc=True,
        )

    def connect_vectordb(self, index_name, index_schema=None):
        vector_db = QdrantVectorStore(
            client=self.client,
            collection_name=index_name,
            embedding=self.embeddings,
            retrieval_mode=RetrievalMode.DENSE,
            schema=index_schema
        )
        return vector_db

    def add_vectordb(self, documents, index_name):
        qdrant = QdrantVectorStore(
            client=self.client,
            collection_name=index_name,
            embedding=self.embeddings,
            retrieval_mode=RetrievalMode.DENSE,
        )
        qdrant.add_documents(documents)
    
    def similarity_search(self, query, k=2, filter=None):
        # Tạo vector store để tìm kiếm
        vector_store = QdrantVectorStore(
            client=self.client,
            collection_name="my_documents",  # Mặc định collection name
            embedding=self.embeddings,
            retrieval_mode=RetrievalMode.DENSE,
        )
        
        # Xử lý filter nếu là danh sách string
        if isinstance(filter, list) and all(isinstance(item, str) for item in filter):
            filter_conditions = []
            for f in filter:
                filter_conditions.append(models.FieldCondition(
                    key="metadata.source",
                    match=models.MatchValue(value=f)
                ))
            qdrant_filter = models.Filter(should=filter_conditions)
        else:
            qdrant_filter = filter
            
        # Thực hiện tìm kiếm
        results = vector_store.similarity_search(
            query, 
            k=k, 
            filter=qdrant_filter
        )
        
        return results
