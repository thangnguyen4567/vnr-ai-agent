from abc import ABC, abstractmethod

import redis

from src.config import settings
from src.vectordb.vectordb import VectorDBManager


class Training(ABC):
    """Lớp cơ sở cho các loại training (course, resource, ...).

    Giữ nguyên logic xử lý như bản Flask cũ, chỉ thay tầng vector database
    sang ``VectorDBManager`` và dùng raw redis client để scan/xóa key theo
    metadata (dedup theo courseid/coursemoduleid).
    """

    def __init__(self):
        self.vector_db = VectorDBManager()
        self.redis_client = self._connect_client()
        self.response = {
            "error": False,
            "message": "",
        }

    def _connect_client(self):
        """Tạo raw redis client để scan/hget/delete key theo metadata."""
        return redis.Redis(
            host=settings.VECTORDB_CONFIG["host"],
            port=int(settings.VECTORDB_CONFIG["port"]),
        )

    def _doc_key_pattern(self, collection):
        """Mẫu pattern key của document trong Redis.

        ``langchain_redis`` lưu key theo dạng ``"{index_name}:{id}"``
        (key_prefix mặc định bằng chính index_name). Bản Flask cũ dùng
        ``"doc:{index}*"`` vì trước đây lưu qua ``langchain_community.Redis``.
        """
        return f"{collection}:*"

    @abstractmethod
    def save_training_data(self, data):
        pass

    @abstractmethod
    def delete_training_data(self, data):
        pass

    @abstractmethod
    def check_training_duplication(self):
        pass

    @abstractmethod
    def get_collection_name(self, data):
        pass
