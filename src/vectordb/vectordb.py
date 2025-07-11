from langchain_qdrant import QdrantVectorStore
from src.config import settings
from langchain_openai import OpenAIEmbeddings
from qdrant_client import QdrantClient
from langchain_qdrant import QdrantVectorStore, RetrievalMode
from langchain_core.documents import Document
from qdrant_client import models

class VectorDBManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(VectorDBManager, cls).__new__(cls)
            cls._instance._init_db()
        return cls._instance

    def _init_db(self):
        # Tạo embedding model
        self.embedding = OpenAIEmbeddings(
            model="text-embedding-3-small", 
            api_key=settings.LLM_CONFIG["openai"]["api_key"]
        )

        client = QdrantClient(
            host=settings.VECTORDB_CONFIG["host"], 
            port=settings.VECTORDB_CONFIG["port"], 
            prefer_grpc=True,
        )

        self.vector_store = QdrantVectorStore(
            client=client,
            collection_name="my_documents_5",
            embedding=self.embedding,
            retrieval_mode=RetrievalMode.DENSE,
        )

    def add_documents(self, documents: list[Document]):
        self.vector_store.add_documents(documents)


    def get_documents(self, query: str, k: int = 2, filter: list[str] = ['tweet']):

        filter_conditions = []
        for f in filter:
            filter_conditions.append(models.FieldCondition(
                key="metadata.source",
                match=models.MatchValue(value=f)
            ))

        import time
        
        # Bắt đầu đo thời gian
        start_time = time.time()
        
        # Thực hiện tìm kiếm
        results = self.vector_store.similarity_search(
            query, 
            k=k, 
            filter=models.Filter(
                should=filter_conditions
            )
        )
        
        # Kết thúc đo thời gian và tính toán
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Thời gian tìm kiếm: {execution_time:.4f} giây")
        
        return results
