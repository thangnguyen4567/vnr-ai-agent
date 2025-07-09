import pytest


def test_chat_process(client):
    """
    Test endpoint chat/process xử lý request và trả về response stream
    """
    # Tạo dữ liệu test
    test_data = {
        "input": {
            "messages": [
                {
                    "role": "user",
                    "content": "test model"
                }
            ]
        },
        "config": {
            "recursion_limit": 10,
            "agent_type": "multi",
            "configurable": {
                "thread_id": "string",
                "agent_id": "d4e12d5bb4014794fa3f956e2b0e01cf",
                "language": "vi-VN",
                "current_date": "string"
            }
        }
    }

    
    # Gọi API với dữ liệu thật
    response = client.post("/chat/process", json=test_data)
    
    # Kiểm tra kết quả
    assert response.status_code == 200