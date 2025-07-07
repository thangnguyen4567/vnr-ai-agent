from typing import Any, Dict, List, Optional
from src.core.nodes.tool_node.formatter.base_formatter import BaseFormatter

class DefaultFormatter(BaseFormatter):
    """
    Default formatter cho các kết quả không phải list/dict
    """
    def format(
        self, 
        result: Any,
        output_params: Optional[List[Dict[str, Any]]] = None,
    ) -> str:

        try:
            if result is None:
                return "No result returned from tool call"
            
            return str(result)
        except Exception as e:
            return f"Error formatting result: {str(e)}"
    
