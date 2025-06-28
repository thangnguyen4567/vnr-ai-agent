from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseToolHandler(ABC):
    
    @abstractmethod
    async def process(self, *args, **kwargs) -> Dict[str, Any]:
        pass

