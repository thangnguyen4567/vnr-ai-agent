from src.core.nodes.tool_node.base_tool_handler import BaseToolHandler
from typing import Any, Dict, List, Tuple
from src.core.nodes.tool_node.formatter import get_formatter
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request
from langchain_core.messages import ToolMessage

class HttpToolHandler(BaseToolHandler):

    async def process(
            self, 
            tool_calls_info: List[Dict[str, Any]], 
            http_tool_registry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process HTTP tool call

        Args:
            tool_call_info: Tool call info
            http_tool: HTTP tool config

        Returns:
            Trạng thái đã cập nhật với kết quả tool call
        """

        try:
            tool_messages = []
            for tool_call_info in tool_calls_info:
                #chuẩn bị tham số cho request
                url, method, params = self._preprare_http_request_params(
                    tool_call_info,
                    http_tool_registry[tool_call_info.get("name")]
                )
                #gửi request và lấy kết quả
                result = await do_async_http_request(
                    url,
                    method,
                    **params
                )

                output_params = http_tool_registry[tool_call_info.get("name")].get("output_params", [])
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
            
    def _preprare_http_request_params(
        self, 
        tool_call_info: Dict[str, Any],
        http_tool: Dict[str, Any]
    ) -> Tuple[str, str, Dict[str, Any]]:
        """
        Prepare HTTP request parameters

        Args:
            tool_call_info: Tool call info
            http_tool: HTTP tool config

        Returns:
            HTTP request parameters
        """
        # Lấy url và method
        url = http_tool.get("url", "") or http_tool.get("tool_path", "")
        method = http_tool.get("method", "GET").upper()

        # Khởi tạo các tham số
        path_params = {}
        headers = {}
        body = {}
        query_params = {}

        input_params = http_tool.get("input_params", {})
        args = tool_call_info.get("args", {})

        # Process default parameters
        path_params, headers, query_params, body = self._process_default_params(
            input_params,
            path_params,
            headers,
            query_params,
            body,
        )

        # Process args parameters from tool call info
        path_params, headers, query_params, body = self._process_tool_args(
            input_params,
            args,
            path_params,
            headers,
            query_params,
            body,
        )

        params = {
            "path_params": path_params,
            "headers": headers,
            "body": body,
            "query_params": query_params
        }

        return url, method, params

    def _process_default_params(
        self,
        input_params: List[Dict[str, Any]],
        path_params: Dict[str, Any],
        headers: Dict[str, Any],
        query_params: Dict[str, Any],
        body: Dict[str, Any],
     ) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any], Dict[str, Any]]:
        """
        Xử lý tham số mặc định từ input_params

        Args:
            input_params: Danh sách tham số của tool
            path_params: Tham số path
            headers: Tham số header
            query_params: Tham số query
            body: Tham số body
        """
        for param in input_params:
            param_name = param.get("name", "")
            param_default = param.get("default", "")
            param_method = param.get("input_method", "").lower()

            if param_default:
                # Phân loại tham số theo input_method
                if param_method == "path":
                    path_params[param_name] = param_default
                elif param_method == "header":
                    headers[param_name] = param_default
                elif param_method == "body":
                    body[param_name] = param_default
                elif param_method == "query":
                    query_params[param_name] = param_default

        return path_params, headers, query_params, body


    def _process_tool_args(
        self,
        input_params: List[Dict[str, Any]],
        args: Dict[str, Any],
        path_params: Dict[str, Any],
        headers: Dict[str, Any],
        query_params: Dict[str, Any],
        body: Dict[str, Any],
    ) -> Tuple[Dict[str, Any], Dict[str, str], Dict[str, Any], Dict[str, Any]]:
        """
        Xử lý tham số từ arguments của tool call 

        Args:
            input_params: Danh sách tham số của tool
            args: Arguments từ tool call 
            path_params: Tham số path
            headers: Tham số header
            query_params: Tham số query
            body: Tham số body

        Returns:
            Path parameters
            Headers
            Query
            Body
        """
        for param in input_params:
            param_name = param.get("name", "")
            param_enabled = param.get("enabled", True)
            param_method = param.get("input_method", "").lower()

            if param_enabled and param_name in args:
                param_value = args[param_name]

                if not param_value:
                    continue
                
                if param_method == "path":
                    path_params[param_name] = param_value
                elif param_method == "header":
                    headers[param_name] = param_value
                elif param_method == "query":
                    query_params[param_name] = param_value
                elif param_method == "body":
                    body[param_name] = param_value

        return path_params, headers, query_params, body
            
            
        
    
