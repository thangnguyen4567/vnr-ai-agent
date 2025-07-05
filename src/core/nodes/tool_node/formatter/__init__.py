from typing import Any

from src.core.nodes.tool_node.formatter.base_formatter import BaseFormatter
from src.core.nodes.tool_node.formatter.default_formatter import DefaultFormatter
from src.core.nodes.tool_node.formatter.dict_formatter import DictFormatter

def get_formatter(result: Any) -> BaseFormatter:
    """
    Lấy formatter phù hợp dựa trên kết quả

    Args:
        result: Kết quả trả về từ tool call

    Returns:
        Formatter phù hợp với kiểu dữ liệu
    """
    if isinstance(result, dict):
        return DictFormatter()
    return DefaultFormatter()