import pytest
import json
from unittest.mock import patch


@pytest.mark.asyncio
@patch("src.api.services.chat_service.ChatService.agent_stream_response")
@patch("src.api.services.chat_service.ChatService.get_langfuse_handler")
def test_chat_process(mock_get_langfuse, mock_stream_response, client):
    """
    Test endpoint chat/process xử lý request và trả về response stream
    """
    # Mock các hàm gọi API
    mock_get_langfuse.return_value = None
    mock_stream_response.return_value = ({"data": json.dumps({"type": "thinking", "content": "test"})} for _ in range(1))
    
    # Tạo dữ liệu test
    test_data = {
        "input": {
            "messages": [
            {
                "role": "user",
                "content": "string"
            }
            ]
        },
        "config": {
            "recursion_limit": 10,
            "agent_type": "multi",
            "metadata": {
            "additionalProp1": {}
            },
            "configurable": {
            "thread_id": "string",
            "agent_id": "d4e12d5bb4014794fa3f956e2b0e01cf",
            "language": "vi-VN",
            "current_date": "string"
            }
        }
    }

    
    # Gọi API
    response = client.post("/chat/process", json=test_data)
    
    # Kiểm tra kết quả
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    # Kiểm tra các hàm đã được gọi
    mock_get_langfuse.assert_called_once()
    mock_stream_response.assert_called_once() 