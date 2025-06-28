from src.core.nodes.tool_node.base_tool_handler import BaseToolHandler
from typing import Any, Dict

class HttpToolHandler(BaseToolHandler):

    async def process(
            self, 
            tool_call_info: dict[str, Any], 
            http_tool: dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process HTTP tool call

        Args:
            tool_call_info: Tool call info
            http_tool: HTTP tool config

        Returns:
            Trạng thái đã cập nhật với kết quả tool call
        """
        tool_name = tool_call_info.get("name","")

        pass

