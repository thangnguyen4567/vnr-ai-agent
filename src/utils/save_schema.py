import json
import os
from typing import List, Dict, Any
from langchain_core.documents import Document
from src.vectordb.vectordb import VectorDBManager

def load_schema_json(file_path: str) -> List[Dict[str, Any]]:
    """Đọc dữ liệu từ file schema.json"""
    with open(file_path, 'r', encoding='utf-8') as file:
        schema_data = json.load(file)
    return schema_data

def convert_to_documents(schema_data: List[Dict[str, Any]]) -> List[Document]:
    """Chuyển đổi dữ liệu schema thành các Document objects"""
    documents = []
    
    # Xử lý từng item trong schema (là một list các dictionary)
    for item in schema_data:
        # Lấy pageId làm id cho document
        page_id = item.get("pageId", "unknown")
        
        # Chuyển đổi object thành text
        content = item.get("description", "") + ' - ID màn hình: ' + page_id
        
        # Tạo metadata để dễ dàng tìm kiếm sau này
        metadata = {
            "pageId": page_id,
            "buttons": json.dumps(item.get("buttons", [])),
            "forms": json.dumps(item.get("forms", [])),
            "grids": json.dumps(item.get("grids", [])),
            "toolbar": json.dumps(item.get("toolbar", [])),
        }
        
        # Tạo document
        doc = Document(page_content=content, metadata=metadata)
        documents.append(doc)
        
    return documents

def save_to_redis_vectordb(documents: List[Document], collection_name: str = "ui_schema"):
    """Lưu documents vào Redis Vector DB"""
    vector_db = VectorDBManager()
    vector_db.delete_index(collection_name)
    vector_db.add_documents(documents, collection_name)
    print(f"Đã lưu {len(documents)} documents vào Redis Vector DB trong collection '{collection_name}'")

def save_schema():
    """Hàm chính để thực thi"""
    # Đường dẫn đến file schema.json
    schema_file_path = "settings/ui_schema.json"
    
    # Kiểm tra file tồn tại
    if not os.path.exists(schema_file_path):
        print(f"Không tìm thấy file {schema_file_path}")
        return
    
    # Đọc dữ liệu từ file schema.json
    print(f"Đang đọc dữ liệu từ {schema_file_path}...")
    schema_data = load_schema_json(schema_file_path)
    
    # Chuyển đổi thành documents
    print("Chuyển đổi dữ liệu thành documents...")
    documents = convert_to_documents(schema_data)
    
    # Lưu vào Redis Vector DB
    print(f"Đang lưu {len(documents)} documents vào Redis Vector DB...")
    save_to_redis_vectordb(documents)
    
    print("Hoàn thành!")
