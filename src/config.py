from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict, Any
from src.utils import ConfigReaderInstance
import os


def load_config_from_file(file_path, file_type = "yaml"):
    """Hàm tải cấu hình từ file và xử lý trường hợp file không tồn tại"""
    if os.path.exists(file_path):
        if file_type == "yaml":
            return ConfigReaderInstance.yaml.read_config_from_file(file_path)
        elif file_type == "txt":
            return ConfigReaderInstance.text.read_config_from_file(file_path)
    return {}


class GlobalConfig(BaseSettings):
    """Cấu hình toàn cục kết hợp cấu hình từ file và biến môi trường"""

    MONGO_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/mongodb.yaml")
    )

    LANGFUSE_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/langfuse.yaml")
    )

    LLM_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/llm.yaml")
    )

    MULTI_AGENT_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/multi_agent.yaml")
    )

    FC_AGENT_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/fc_agent.yaml")
    )
    
    HRM_PROMPT: str = Field(
        default_factory=lambda: load_config_from_file("settings/prompt/hrm_prompt.txt", "txt")
    )


# Khởi tạo cấu hình toàn cục
settings = GlobalConfig()
