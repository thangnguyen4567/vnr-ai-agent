import os
from typing import Dict, Any
from src.config import settings


class AgentConfigLoader:
    _instance = None
    _multi_config = None
    _current_agent_type = None
    _default_agent_id = None
    _agent_project_code = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AgentConfigLoader, cls).__new__(cls)
            cls._instance._load_config()
        return cls._instance

    def _load_config(self) -> Dict[str, Any]:
        """Load cấu hình agent"""
        # Thiết lập mã dự án mặc định
        self._agent_project_code = "default"
        self._multi_config_project = settings.MULTI_AGENT_CONFIG

        if "default" in self._multi_config_project:
            self._multi_default_agent = self._multi_config_project["default"]

    def get_agent_project_code(self) -> str:
        """Lấy mã dự án hiện tại"""
        return self._agent_project_code

    def set_agent_project(self, agent_project_code: str = "default"):
        """Thiết lập loại agent hiện tại"""
        self._agent_project_code = agent_project_code
        # Lấy cấu hình agent mặc định
        self._multi_default_agent = self._multi_config_project[agent_project_code]


    def get_config_for_agent_id(self, agent_id: str = None) -> Dict[str, Any]:

        # Lấy cấu hình agent mặc định
        current_config = self._multi_default_agent

        if agent_id == current_config.get("agent_id"):
            # Nếu agent_id trùng với agent_id mặc định thì trả về cấu hình agent mặc định
            return current_config
        else:
            # Nếu agent_id không trùng với agent_id mặc định thì kiểm tra trong sub_agents
            if agent_id in current_config.get("agent_id"):
                return current_config

            # Nếu agent_id không trùng với agent_id mặc định thì kiểm tra trong sub_agents
            sub_agents = current_config.get("sub_agents", {})
            for sub_agent in sub_agents:
                if sub_agent.get("agent_id") == agent_id:
                    return sub_agent

            return current_config


agent_config_loader = AgentConfigLoader()
