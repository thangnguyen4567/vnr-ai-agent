from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict, Any
from src.utils import ConfigReaderInstance
import os


def load_config_from_file(file_path):
    """Hàm tải cấu hình từ file và xử lý trường hợp file không tồn tại"""
    if os.path.exists(file_path):
        return ConfigReaderInstance.yaml.read_config_from_file(file_path)
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


# Khởi tạo cấu hình toàn cục
settings = GlobalConfig()
