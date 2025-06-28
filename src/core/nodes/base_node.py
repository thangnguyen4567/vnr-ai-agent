from abc import ABC, abstractmethod
from typing import Any, Dict
from langchain_core.runnables import RunnableConfig

class BaseNode(ABC):

    @abstractmethod
    async def process(self, state: Dict[str, Any], config: RunnableConfig) -> Dict[str, Any]:
        pass
    