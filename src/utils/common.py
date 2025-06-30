import os
from enum import Enum


class AgentType(Enum):
    """Loại agent"""

    SINGLE_AGENT = "single"
    MULTI_AGENT = "multi"
