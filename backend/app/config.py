from pydantic_settings import BaseSettings
from pydantic import ConfigDict

class Settings(BaseSettings):
    SECRET_KEY: str = "dev_secret_key_change_in_prod"
    DATABASE_URL: str = "sqlite+aiosqlite:///./leaderai.db"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "password"
    
    model_config = ConfigDict(env_file=".env")

settings = Settings()

