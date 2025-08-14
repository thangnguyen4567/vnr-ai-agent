from src.core import AgentState
from langchain_core.runnables import RunnableConfig
from src.core.nodes.utils.tool_utils import extract_tool_call_info, get_agent_config
from src.core.nodes.tool_node.http_tool_handler import HttpToolHandler 
from src.core.nodes.tool_node.builtin_tool_handler import BuiltinToolHandler
from src.core.nodes.tool_node.store_tool_handler import StoreToolHandler
from src.core.nodes.tool_node.workflow_tool_handler import WorkflowToolHandler

# Khởi tạo các handler cho các tool
builtin_tool_handler = BuiltinToolHandler()
http_tool_handler = HttpToolHandler()
store_tool_handler = StoreToolHandler()
workflow_tool_handler = WorkflowToolHandler()   

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
        # Lấy thông tin tool call từ state ( được AI tạo ra )
        tool_calls_info = extract_tool_call_info(state)
        if not tool_calls_info:
            return await builtin_tool_handler.process(state, None)
        
        # Lấy cấu hình tool từ state
        for tool_call_info in tool_calls_info:
            tool_name = tool_call_info.get("name")
            agent_config = get_agent_config(state)
            # Lấy các cấu hình tool từ state của agent
            http_tool_registry = agent_config.get("http_tool_registry", {})
            store_tool_registry = agent_config.get("store_tool_registry", {})
            workflow_tool_registry = agent_config.get("workflow_tool_registry", {})
            #Phân loại tool theo type
            if tool_name in http_tool_registry:
                return await http_tool_handler.process(tool_calls_info, http_tool_registry)
            elif tool_name in store_tool_registry:
                return await store_tool_handler.process(tool_calls_info, store_tool_registry)
            elif tool_name in workflow_tool_registry:
                return await workflow_tool_handler.process(tool_calls_info, workflow_tool_registry)
            else:
                return await builtin_tool_handler.process(state, tool_call_info)
            
    except Exception as e:
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



