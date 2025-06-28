import logging
from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from src.core.nodes.tool_node.utils import extract_tool_call_info, get_agent_config
from src.core.nodes.tool_node.http_tool_handler import HttpToolHandler 
from src.core.nodes.tool_node.builtin_tool_handler import BuiltinToolHandler

logger = logging.getLogger(__name__)

builtin_tool_handler = BuiltinToolHandler()
http_tool_handler = HttpToolHandler()

async def tool_call(state: AgentState, config: RunnableConfig):
    """
    Process tool call và trả về kết quả

    Args:
        state: AgentState
        config: RunnableConfig

    Returns:
        Trạng thái đã cập nhật với kết quả tool call
    """

    tool_call_info = None
    try:
        tool_calls_info = extract_tool_call_info(state)
        if not tool_calls_info:
            logger.info("No tool call info found, using default toolNode")
            return await builtin_tool_handler.process(state, None)
        
        for tool_call_info in tool_calls_info:
            tool_name = tool_call_info.get("name")
            agent_config = get_agent_config(state)
            http_tool_registry = agent_config.get("http_tool_registry", {})
            
            #Phân loại tool
            if tool_name in http_tool_registry:
                return await http_tool_handler.process(tool_call_info, http_tool_registry[tool_name])
            else:
                return await builtin_tool_handler.process(state, tool_call_info)
            
    except Exception as e:
        logger.error(f"Error processing tool call: {e}")
        return {
            "messages": [
                {
                    "role": "tool",
                    "tool_call_id": tool_call_info.get("id") if tool_call_info else "",
                    "name": tool_call_info.get("name") if tool_call_info else "unknown_tool",
                    "content": f"Error processing tool call: {e}"
                }
            ]
        }



