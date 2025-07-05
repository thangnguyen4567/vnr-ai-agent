import json
from typing import Any, Dict, List, Optional
from src.core.nodes.tool_node.formatter.base_formatter import BaseFormatter

MAX_CONTENT_LENGTH = 15000

class DictFormatter(BaseFormatter):
    """
    Default formatter cho các kết quả là dict
    """
    def format(
        self, 
        result: Dict[str, Any],
        output_params: Optional[List[Dict[str, Any]]] = None,
        tool_name: Optional[str] = None,
        provider: Optional[str] = None
    ) -> str:

        try:
            filter_result = self._filter_and_format_result(result, output_params)

            return json.dumps(filter_result, ensure_ascii=False, indent=2)
            
        except Exception as e:
            return str(result)
    
    def _filter_and_format_result(
        self,
        result: Dict[str, Any],
        output_params: Optional[List[Dict[str, Any]]] = None
    ) -> Dict[str, Any]:
        """
        Filter và format kết quả

        Args:
            result: Kết quả trả về từ tool call
            output_params: Danh sách tham số output

        Returns:
            Kết quả đã được filter và format
        """

        filtered_result = {}
        instructions = []
        if output_params:
            for param in output_params:
                param_name = param.get("name", "")
                param_enabled = param.get("enabled", True)
                param_description = param.get("description", "")

                if param_enabled and param_name in result:
                    value = result[param_name]
                    if isinstance(value, dict):
                        filtered_result[param_name] = value[:MAX_CONTENT_LENGTH]
                    else:
                        filtered_result[param_name] = value

                    # Thêm instructions nếu có description
                    if param_description:
                        instructions.append(f"Output {param_name}: {param_description}")
       
        else:
            for key, value in result.items():
                if isinstance(value, dict):
                    filtered_result[key] = value[:MAX_CONTENT_LENGTH]
                else:
                    filtered_result[key] = value

        # Thêm instructions nếu có
        if instructions:
            return {
                "instructions": "\n".join(instructions),
                **filtered_result
            }

        return filtered_result

