import os
from typing import Dict, Any
from src.config import settings


class AgentConfigLoader:
    _instance = None
    _fc_config = None
    _multi_config = None
    _current_agent_type = None
    _default_agent_id = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentConfigLoader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> Dict[str, Any]:
        self._fc_config = settings.FC_AGENT_CONFIG
        self._multi_config = settings.MULTI_AGENT_CONFIG

        if self._fc_config and "agent_id" in self._fc_config:
            self._fc_default_agent_id = self._fc_config["agent_id"]

        if self._multi_config and "agent_id" in self._multi_config:
            self._multi_default_agent_id = self._multi_config["agent_id"]

    def set_agent_type(self, agent_type: str):
        """Thiết lập loại agent hiện tại"""
        if agent_type not in ["fc", "multi"]:
            raise ValueError("Invalid agent type")
        self._current_agent_type = agent_type

        if agent_type == "fc" and hasattr(self, "_fc_default_agent_id"):
            self._fc_default_agent_id = self._fc_default_agent_id
        elif agent_type == "multi" and hasattr(self, "_multi_default_agent_id"):
            self._fc_default_agent_id = self._multi_default_agent_id

    def get_agent_type(self) -> str:
        return self._current_agent_type

    def get_current_config(self) -> Dict[str, Any]:
        """Lấy cấu hình agent hiện tại"""
        if self._current_agent_type == "fc":
            return self._fc_config
        elif self._current_agent_type == "multi":
            return self._multi_config
        else:
            raise ValueError("Invalid agent type")

    def get_default_agent_id(self) -> str:

        if not self._default_agent_id:

            current_config = self.get_current_config()
            self._default_agent_id = current_config.get("agent_id")

        return self._default_agent_id

    def get_config_for_agent_id(self, agent_id: str = None) -> Dict[str, Any]:

        if agent_id is None:
            agent_id = self.get_default_agent_id()

        current_config = self.get_current_config()

        if self._current_agent_type == "fc":
            return current_config
        else:
            if agent_id == current_config.get("agent_id"):
                return current_config
            else:
                if agent_id in current_config.get("agent_id"):
                    return current_config

                sub_agents = current_config.get("sub_agents", {})
                for sub_agent in sub_agents:
                    if sub_agent.get("agent_id") == agent_id:
                        return sub_agent

                return current_config


agent_config_loader = AgentConfigLoader()
