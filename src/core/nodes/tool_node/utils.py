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