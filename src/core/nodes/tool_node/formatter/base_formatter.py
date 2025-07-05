from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional

class BaseFormatter(ABC):
    @abstractmethod
    def format(
        self, 
        result: Any,
        output_params: Optional[List[Dict[str, Any]]] = None,
        tool_name: Optional[str] = None,
        provider: Optional[str] = None
    ) -> str:
        """
        Format kết quả trả về từ tool call thành chuỗi

        Args:
            result: Kết quả trả về từ tool call
            output_params: Danh sách tham số output
            tool_name: Tên tool
            provider: Nhà cung cấp

        Returns:
            Chuỗi kết quả đã được format
        """
        pass
    
