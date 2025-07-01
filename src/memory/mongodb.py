import os
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver
from src.config import settings


def get_mongodb_checkpointer():
    """
    Tạo MongoDB checkpointer từ cấu hình

    Returns:
        MongoDBSaver: MongoDB checkpointer
    """
    mongo_client = MongoClient(
        host=settings.MONGO_CONFIG["connection"]["host"],
        username=settings.MONGO_CONFIG["connection"]["username"],
        password=settings.MONGO_CONFIG["connection"]["password"],
    )
    return MongoDBSaver(mongo_client)
