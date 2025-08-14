from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BaseToolHandler(ABC):
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        pass

    @abstractmethod
    def _preprare_request_params(self, *args, **kwargs) -> Tuple[str, str, Dict[str, Any]]:
        pass

    @abstractmethod
    def _process_default_params(self, *args, **kwargs) -> Tuple[str, str, Dict[str, Any]]:
        pass

    @abstractmethod
    def _process_tool_args(self, *args, **kwargs) -> Tuple[str, str, Dict[str, Any]]:
        pass