from pydantic import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    app_env: str = "development"
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    database_url: str
    google_application_credentials: str
    api_key: str
    admin_email: str

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings() 