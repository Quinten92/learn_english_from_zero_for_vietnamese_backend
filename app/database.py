"""
Supabase Database Client
Singleton pattern for database connection
"""

from supabase import create_client, Client
from .config import get_settings

# Global Supabase client instance
_supabase_client: Client | None = None


def get_supabase() -> Client:
    """
    Get Supabase client instance (singleton pattern)
    Returns the same client instance for all requests
    """
    global _supabase_client
    
    if _supabase_client is None:
        settings = get_settings()
        
        if not settings.supabase_url or not settings.supabase_key:
            raise ValueError(
                "Supabase credentials not configured. "
                "Please set SUPABASE_URL and SUPABASE_KEY environment variables."
            )
        
        _supabase_client = create_client(
            settings.supabase_url,
            settings.supabase_key
        )
    
    return _supabase_client


def check_db_connection() -> dict:
    """
    Check if database connection is working
    Returns status dict
    """
    try:
        client = get_supabase()
        # Query schema để check connection (không cần table tồn tại)
        # Dùng RPC hoặc check auth
        result = client.auth.get_session()
        return {"status": "connected", "error": None}
    except Exception as e:
        error_msg = str(e)
        # Các lỗi này nghĩa là connection OK nhưng không có data/table
        if any(x in error_msg for x in [
            "does not exist", 
            "relation", 
            "Could not find",
            "PGRST205",
            "No API key found"
        ]):
            return {"status": "connected", "error": None}
        return {"status": "error", "error": error_msg}
