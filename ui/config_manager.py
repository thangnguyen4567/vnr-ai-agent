import os
import uuid
from typing import Dict, Any

import streamlit as st
import yaml

from src.config import settings
import requests

class ConfigManager:
    """Lớp quản lý cấu hình"""

    def __init__(self, config_path: str):
        """Khởi tạo ConfigManager với đường dẫn file cấu hình"""
        self.config_path = config_path

        if "agent_config" not in st.session_state:
            st.session_state.agent_config = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """Load cấu hình từ file YAML"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as file:
                    config = yaml.safe_load(file)
                    if "settings" not in config:
                        config["settings"] = {
                            "auth_method": "oauth2",
                            "token": "",
                            "url_endpoint": "http://localhost:8000/",
                            "workflow_url": "http://localhost:8000/",
                            "token_url": "",
                            "client_id": "",
                            "client_secret": "",
                            "username": "",
                            "password": "",
                        }
                    if config:
                        return config
        except Exception as e:
            st.error(f"Lỗi khi đọc file cấu hình: {str(e)}")

        # Cấu hình mặc định nếu không load được
        return {
            "agent_id": str(uuid.uuid4()),
            "name": "Multi Agent",
            "type": "multi",
            "sub_agents": [],
            "settings": {
                "auth_method": "oauth2",
                "token": "",
                "url_endpoint": "http://localhost:8000/",
            },
        }

    def save_config(self) -> bool:
        """Lưu cấu hình vào file YAML"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(
                    st.session_state.agent_config,
                    file,
                    default_flow_style=False,
                    allow_unicode=True,
                    sort_keys=False,
                )

            settings.reload_multi_agent_config()
            requests.get("http://agent-api:8000/update-config")
            return True
        except Exception as e:
            st.error(f"Lỗi khi lưu cấu hình: {str(e)}")
            return False

    def create_sub_agent(self):
        """Tạo một sub-agent mới"""
        new_id = str(uuid.uuid4())
        st.session_state.agent_config["sub_agents"].append(
            {
                "agent_id": new_id,
                "name": "New Agent",
                "description": "",
                "type": "fc",
                "nodes": {
                    "llm": {"provider": "openai", "agent_prompt": ""},
                    "tools": [],
                },
            }
        )
        self.save_config()

    def delete_sub_agent(self, idx: int):
        """Xóa một sub-agent theo index"""
        if 0 <= idx < len(st.session_state.agent_config.get("sub_agents", [])):
            st.session_state.agent_config["sub_agents"].pop(idx)
            self.save_config()

    def create_tool(self, agent_idx: int):
        """Thêm một tool mới cho agent"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if "nodes" not in agent:
                agent["nodes"] = {
                    "llm": {"provider": "openai", "agent_prompt": ""},
                    "tools": [],
                }
            elif "tools" not in agent["nodes"]:
                agent["nodes"]["tools"] = []

            agent["nodes"]["tools"].append(
                {
                    "type": "http",
                    "name": "new_tool",
                    "description": "",
                    "tool_path": "",
                    "input_params": [],
                }
            )
            self.save_config()

    def delete_tool(self, agent_idx: int, tool_idx: int):
        """Xóa một tool khỏi agent"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if (
                "nodes" in agent
                and "tools" in agent["nodes"]
                and 0 <= tool_idx < len(agent["nodes"]["tools"])
            ):
                agent["nodes"]["tools"].pop(tool_idx)
                self.save_config()

    def create_param(self, agent_idx: int, tool_idx: int):
        """Thêm một parameter mới cho tool"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if (
                "nodes" in agent
                and "tools" in agent["nodes"]
                and 0 <= tool_idx < len(agent["nodes"]["tools"])
            ):
                tool = agent["nodes"]["tools"][tool_idx]
                if "input_params" not in tool:
                    tool["input_params"] = []

                tool["input_params"].append(
                    {
                        "name": "",
                        "description": "",
                        "input_method": "query",
                        "type": "string",
                        "default": "",
                        "required": False,
                    }
                )
                self.save_config()

    def delete_param(self, agent_idx: int, tool_idx: int, param_idx: int):
        """Xóa một parameter khỏi tool"""
        if 0 <= agent_idx < len(st.session_state.agent_config.get("sub_agents", [])):
            agent = st.session_state.agent_config["sub_agents"][agent_idx]
            if (
                "nodes" in agent
                and "tools" in agent["nodes"]
                and 0 <= tool_idx < len(agent["nodes"]["tools"])
            ):
                tool = agent["nodes"]["tools"][tool_idx]
                if "input_params" in tool and 0 <= param_idx < len(tool["input_params"]):
                    tool["input_params"].pop(param_idx)
                    self.save_config()

    def get_config(self) -> Dict[str, Any]:
        """Lấy cấu hình hiện tại"""
        return st.session_state.agent_config

    def get_yaml_string(self) -> str:
        """Chuyển đổi cấu hình hiện tại thành chuỗi YAML"""
        return yaml.dump(
            st.session_state.agent_config,
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )


