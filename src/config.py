from pydantic import BaseModel
from pydantic_settings import BaseSettings

class AppConfig(BaseModel):
    pass

class GlobalConfig(BaseSettings):
    APP_CONFIG: AppConfig = AppConfig()