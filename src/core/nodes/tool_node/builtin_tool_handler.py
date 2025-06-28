from src.core.nodes.tool_node.base_tool_handler import BaseToolHandler
from src.core.tools.builtin_tool import built_in_tools
from langgraph.prebuilt import ToolNode
from typing import Optional, Dict, Any
from src.core import AgentState
from src.core.nodes.utils.message_utils import create_error_response

class BuiltinToolHandler(BaseToolHandler):
    """
        Handler xử lý các tool built-in 
    """
    def __init__(self):
        self.tool_node = ToolNode(built_in_tools)

    async def process(
            self,
            state: AgentState,
            tool_call_info: Optional[Dict[str, Any]] = None,
        ) -> Dict[str, Any]:
        """
        Xử lý tool call

        Args:
            state: Trạng thái hiện tại của agent
            tool_call_info: Thông tin tool call ( có thể là None)

        Returns:
            Trạng thái mới của agent sau khi xử lý tool call
        """
        try:
            # Sử dụng tool node để xử lý tool call
            result = await self.tool_node.ainvoke(state)
            return result
        
        except Exception as e:
            return create_error_response(
                tool_call_info,
                f"Error processing tool call: {e}"
            )
