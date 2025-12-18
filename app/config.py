"""
Application Configuration
Load settings from environment variables
"""

from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Supabase Configuration
    supabase_url: str = ""
    supabase_key: str = ""  # anon/public key
    
    # App Configuration
    app_name: str = "Learn English API"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Cache settings to avoid reading .env file multiple times"""
    return Settings()
