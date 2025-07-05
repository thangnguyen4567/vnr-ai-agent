from typing import Any, Dict, Optional
import logging
from src.core import AgentState

logger = logging.getLogger(__name__)

def extract_tool_call_info(state: AgentState) -> Optional[Dict[str, Any]]:
    """
    Trích xuất thông tin tool call từ message cuối cùng của state

    Args:
        state: Trạng thái hiện tại của agent

    Returns:
        Thông tin tool call hoặc None nếu không tìm thấy
    """
    try:
        last_message = state.get("messages", [])[-1]
        tool_calls = last_message.tool_calls if hasattr(last_message, "tool_calls") else []

        if not tool_calls:
            logger.info("No tool call info found")
            return None
        
        return tool_calls
    
    except Exception as e:
        logger.error(f"Error extracting tool call info: {e}")
        return None
    
def get_agent_config(state: AgentState) -> Dict[str, Any]:
    """
    Lấy cấu hình agent từ state

    Args:
        state: Trạng thái hiện tại của agent

    Returns:
        Cấu hình agent
    """
    agent_id = state.get("agent_id")
    agent_config = state.get("configs", {}).get(agent_id, {}) or {}
    return agent_config
    

def create_tool_response(tool_call_info: dict[str, Any], content: str) -> Dict[str, Any]:
    """
    Tạo response cho tool call

    Args:
        tool_call_info: Thông tin tool call
        content: Nội dung response

    Returns:
        Response cho tool call
    """
    return {
        "messages": [
            {
                "role": "tool",
                "tool_call_id": tool_call_info.get("id"),
                "name": tool_call_info.get("name"),
                "content": content
            }
        ]
    }

def create_error_response(tool_call_info: Optional[Dict[str, Any]], error_message: str) -> Dict[str, Any]:
    """
    Tạo response lỗi cho tool call

    Args:
        tool_call_info: Thông tin tool call
        error_message: Thông báo lỗi

    Returns:
        Response lỗi cho tool call
    """
    if tool_call_info:
        return create_tool_response(tool_call_info, error_message)
    else:
        return {
            "messages": [
                {
                    "role": "tool",
                    "tool_call_id": "",
                    "name": "unknown_tool",
                    "content": error_message
                }
            ]
        }
