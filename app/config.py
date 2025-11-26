from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    SECRET_KEY: str = "dev_secret_key_change_in_prod"
    DATABASE_URL: str = "sqlite+aiosqlite:///./leaderai.db"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "password"
    OPENAI_API_KEY: Optional[str] = None
    ENVIRONMENT: str = "development"
    
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
