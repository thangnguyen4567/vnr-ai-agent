from src.core.nodes.tool_node.base_tool_handler import BaseToolHandler
from typing import Any, Dict, List, Tuple
from src.core.nodes.tool_node.formatter import get_formatter
from src.core.tools.builtin_tool.http_workflow_runner import do_async_http_workflow_request
from langchain_core.messages import ToolMessage

class WorkflowToolHandler(BaseToolHandler):

    async def process(
            self, 
            tool_calls_info: List[Dict[str, Any]], 
            tool_registry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process Workflow tool call

        Args:
            tool_call_info: Tool call info
            tool_registry: Workflow tool config

        Returns:
            Trạng thái đã cập nhật với kết quả tool call
        """

        try:
            tool_messages = []
            for tool_call_info in tool_calls_info:
                # Lấy cấu hình tool theo tool name 
                workflow_tool = tool_registry[tool_call_info.get("name")]
                #chuẩn bị tham số cho request
                params = self._preprare_request_params(
                    tool_call_info,
                    workflow_tool
                )
                headers = {
                    "Content-Type": "application/json",
                    "Authorization": "Bearer " + workflow_tool.get("token_workflow", "")
                }
                #gửi request và lấy kết quả
                result = await do_async_http_workflow_request(
                    url=workflow_tool.get("url", ""),
                    query_params=params,
                    headers=headers,
                )

                output_params = workflow_tool.get("output_params", [])
                formatter = get_formatter(result.data)
                #format kết quả theo output_params và đưa về dạng string
                result_str = formatter.format(
                    result.data,
                    output_params
                )
                
                tool_message = ToolMessage(
                    tool_call_id=tool_call_info.get("id"),
                    name=tool_call_info.get("name"),
                    content=result_str
                )   

                #format theo chuẩn của tool call
                tool_messages.append(tool_message)
        except Exception as e:
            #format theo chuẩn của tool call
            tool_message = ToolMessage(
                tool_call_id="",
                name="unknown_tool",
                content=str(e)
            )
            
        return {
            # Nếu có nhiều hơn 1 tool message thì trả về tool_messages, nếu không thì trả về tool_message
            "messages": tool_messages if len(tool_messages) > 1 else tool_message
        }
            
    def _preprare_request_params(
        self, 
        tool_call_info: Dict[str, Any],
        tool_registry: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Prepare HTTP request parameters

        Args:
            tool_call_info: Tool call info
            http_tool: HTTP tool config

        Returns:
            HTTP request parameters
        """

        # Khởi tạo các tham số
        query_params = {}

        input_params = tool_registry.get("input_params", {})
        args = tool_call_info.get("args", {})

        # Process default parameters
        query_params = self._process_default_params(
            input_params,
            query_params,
        )

        # Process args parameters from tool call info
        query_params = self._process_tool_args(
            input_params,
            args,
            query_params,
        )

        params = {
            "inputs": query_params,
            "query": "no query",
            "response_mode": "blocking",
            "conversation_id": "",
            "user": "nouser",
            "files": []
        }

        return params

    def _process_default_params(
        self,
        input_params: List[Dict[str, Any]],
        query_params: Dict[str, Any],
     ) -> Dict[str, Any]:
        """
        Xử lý tham số mặc định từ input_params

        Args:
            input_params: Danh sách tham số của tool
            query_params: Tham số query
        """
        for param in input_params:
            param_name = param.get("name", "")
            param_default = param.get("default", "")

            if param_default:
                # Phân loại tham số theo input_method
                query_params[param_name] = param_default

        return query_params


    def _process_tool_args(
        self,
        input_params: List[Dict[str, Any]],
        args: Dict[str, Any],
        query_params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Xử lý tham số từ arguments mà AI truyền vào tool call 

        Args:
            input_params: Danh sách tham số của tool
            args: Arguments từ tool call 
            query_params: Tham số query

        Returns:
            Query parameters
        """
        for param in input_params:
            param_name = param.get("name", "")
            param_enabled = param.get("enabled", True)

            if param_enabled and param_name in args:
                param_value = args[param_name]

                if not param_value:
                    continue
                
                query_params[param_name] = param_value

        return query_params
            
            
        
    
