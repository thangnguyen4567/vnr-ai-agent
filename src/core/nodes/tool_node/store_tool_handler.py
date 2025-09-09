from src.core.nodes.tool_node.base_tool_handler import BaseToolHandler
from typing import Any, Dict, List, Tuple
from src.core.nodes.tool_node.formatter import get_formatter
from src.core.tools.builtin_tool.http_request_runner import do_async_http_request
from langchain_core.messages import ToolMessage

class StoreToolHandler(BaseToolHandler):

    async def process(
            self, 
            tool_calls_info: List[Dict[str, Any]], 
            tool_registry: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process Dynamically store tool call

        Args:
            tool_call_info: Tool call info
            http_tool: HTTP tool config

        Returns:
            Trạng thái đã cập nhật với kết quả tool call
        """

        try:
            tool_messages = []
            for tool_call_info in tool_calls_info:
                # Lấy cấu hình tool theo tool name 
                store_tool = tool_registry[tool_call_info.get("name")]
                #chuẩn bị tham số cho request
                params = self._preprare_request_params(
                    tool_call_info,
                    store_tool
                )
                #parse auth_method và auth_params
                auth_method = store_tool.get("auth_method", "bearer")
                auth_params = store_tool.get("auth_params", {})
                #gửi request và lấy kết quả
                result = await do_async_http_request(
                    store_tool.get("url", ""),
                    store_tool.get("method", "POST"),
                    query_params=params,
                    auth_method=auth_method,
                    auth_params=auth_params
                )

                output_params = store_tool.get("output_params", [])
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
        store_tool: Dict[str, Any]
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

        input_params = store_tool.get("input_params", {})
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
        # Lấy page và pageSize từ query_params
        page = query_params.get("page", 1)
        pageSize = query_params.get("pageSize", 5)
    
        params = {
            "DataFormSearch": query_params,
            "StoreName": store_tool.get("store_name", ""),
            "dataSourceRequestString": f"page={page}&pageSize={pageSize}"
        }

        return params

    def _process_default_params(
        self,
        input_params: List[Dict[str, Any]],
        query_params: Dict[str, Any],
     ) -> Dict[str, Any]:
        """
        Xử lý tham số từ arguments mà AI truyền vào tool call 

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
        Xử lý tham số từ arguments của tool call 

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