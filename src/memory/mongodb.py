import os
from pymongo import MongoClient
from langgraph.checkpoint.mongodb import MongoDBSaver


def get_mongodb_checkpointer():
    """
    Tạo MongoDB checkpointer từ biến môi trường

    Returns:
        MongoDBSaver: MongoDB checkpointer
    """
    mongodb_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    mongo_client = MongoClient(mongodb_uri)
    return MongoDBSaver(mongo_client)
