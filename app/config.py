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
    
    # Database Configuration (PostgreSQL direct connection for SQLAlchemy/Alembic)
    database_url: str = ""  # postgresql://user:pass@host:port/db
    
    # Frontend URL (for OAuth redirects)
    frontend_url: str = "http://localhost:3000"
    
    # App Configuration
    app_name: str = "Learn English API"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
    
    @property
    def async_database_url(self) -> str:
        """Convert to async URL for SQLAlchemy async"""
        if self.database_url.startswith("postgresql://"):
            return self.database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self.database_url


@lru_cache()
def get_settings() -> Settings:
    """Cache settings to avoid reading .env file multiple times"""
    return Settings()
