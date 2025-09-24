from pydantic import Field
from pydantic_settings import BaseSettings
from typing import Dict, Any, List
from src.utils import ConfigReaderInstance
import os


def load_config_from_file(file_path):
    """Hàm tải cấu hình từ file và xử lý trường hợp file không tồn tại"""
    if os.path.exists(file_path):
        return ConfigReaderInstance.yaml.read_config_from_file(file_path)
    
    return {}

def load_multi_agent_configs_from_dir(target_dir: str) -> Dict[str, Any]:
    """Load tất cả config multi-agent trong thư mục, trả về dict theo tiền tố file.

    - Ưu tiên thư mục đầu tiên tồn tại trong dir_candidates.
    - Key là tiền tố trước chuỗi "_multi_agent.yaml".
    - Giữ tương thích ngược: ánh xạ cấu hình mặc định vào các khóa top-level
      như 'settings', 'agent_id', 'name', 'type', 'sub_agents' và 'auth'.
    """

    if target_dir is None:
        return {}

    result: Dict[str, Any] = {}
    try:
        files = [f for f in os.listdir(target_dir) if f.endswith("_multi_agent.yaml")]
        files.sort()
        for file_name in files:
            prefix = file_name.rsplit("_multi_agent.yaml", 1)[0]
            cfg = load_config_from_file(os.path.join(target_dir, file_name)) or {}
            # Bảo vệ null key
            if isinstance(cfg, dict):
                result[prefix] = cfg
    except Exception:
        return result

    if not result:
        return {}

    return result


class GlobalConfig(BaseSettings):
    """Cấu hình toàn cục kết hợp cấu hình từ file và biến môi trường"""

    LANGFUSE_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/langfuse.yaml")
    )

    LLM_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/llm.yaml")
    )
    
    MULTI_AGENT_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_multi_agent_configs_from_dir("settings/multi_agents")
    )

    # MULTI_AGENT_CONFIG: Dict[str, Any] = Field(
    #     default_factory=lambda: load_config_from_file("settings/prod_multi_agent.yaml")
    # )

    FC_AGENT_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/fc_agent.yaml")
    )

    VECTORDB_CONFIG: Dict[str, Any] = Field(
        default_factory=lambda: load_config_from_file("settings/vectordb.yaml")
    )

    DEV_MODE: bool = Field(
        default=True
    )

    API_TOKEN: str = Field(
        default=""
    )

    def reload_multi_agent_config(self):
        self.MULTI_AGENT_CONFIG = load_multi_agent_configs_from_dir("settings/multi_agents")
        # self.MULTI_AGENT_CONFIG: Dict[str, Any] = Field(
        #     default_factory=lambda: load_config_from_file("settings/prod_multi_agent.yaml")
        # )
    
    def update_api_token(self, token: str):
        self.API_TOKEN = token
    
# Khởi tạo cấu hình toàn cục
settings = GlobalConfig()
