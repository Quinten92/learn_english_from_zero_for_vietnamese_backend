"""
Auth Router
Handles authentication endpoints using Supabase Auth
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.responses import RedirectResponse
from typing import Optional
import httpx

from ..database import get_supabase
from ..config import get_settings

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={401: {"description": "Unauthorized"}},
)


@router.get("/login/google")
async def login_with_google(redirect_to: Optional[str] = None):
    """
    Get Google OAuth login URL
    
    - **redirect_to**: Optional URL to redirect after successful login
    """
    settings = get_settings()
    supabase = get_supabase()
    
    # Default redirect URL
    redirect_url = redirect_to or f"{settings.frontend_url}/auth/callback"
    
    try:
        # Get OAuth URL from Supabase
        response = supabase.auth.sign_in_with_oauth({
            "provider": "google",
            "options": {
                "redirect_to": redirect_url
            }
        })
        
        return {
            "url": response.url,
            "message": "Redirect to this URL to authenticate with Google"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate OAuth URL: {str(e)}")


@router.get("/callback")
async def auth_callback(
    code: Optional[str] = None,
    error: Optional[str] = None,
    error_description: Optional[str] = None
):
    """
    Handle OAuth callback from Supabase
    
    This endpoint receives the auth code and exchanges it for a session.
    In practice, the frontend handles this, but this can be used for server-side auth.
    """
    if error:
        raise HTTPException(
            status_code=400, 
            detail=f"OAuth error: {error} - {error_description}"
        )
    
    if not code:
        raise HTTPException(status_code=400, detail="No authorization code provided")
    
    try:
        supabase = get_supabase()
        
        # Exchange code for session
        response = supabase.auth.exchange_code_for_session({"auth_code": code})
        
        return {
            "message": "Authentication successful",
            "user": {
                "id": response.user.id,
                "email": response.user.email,
                "full_name": response.user.user_metadata.get("full_name"),
                "avatar_url": response.user.user_metadata.get("avatar_url"),
            },
            "session": {
                "access_token": response.session.access_token,
                "refresh_token": response.session.refresh_token,
                "expires_in": response.session.expires_in,
            }
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Failed to authenticate: {str(e)}")


@router.get("/me")
async def get_current_user(authorization: str = None, request: Request = None):
    """
    Get current authenticated user info
    
    Requires Bearer token in Authorization header
    """
    # Get token from header
    auth_header = request.headers.get("Authorization") if request else authorization
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header. Use: Bearer <token>"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        supabase = get_supabase()
        
        # Verify token and get user
        response = supabase.auth.get_user(token)
        
        if not response.user:
            raise HTTPException(status_code=401, detail="Invalid or expired token")
        
        user = response.user
        return {
            "id": user.id,
            "email": user.email,
            "full_name": user.user_metadata.get("full_name"),
            "avatar_url": user.user_metadata.get("avatar_url"),
            "email_verified": user.email_confirmed_at is not None,
            "created_at": user.created_at,
            "last_sign_in": user.last_sign_in_at,
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Authentication failed: {str(e)}")


@router.post("/logout")
async def logout(request: Request):
    """
    Logout current user
    
    Requires Bearer token in Authorization header
    """
    auth_header = request.headers.get("Authorization")
    
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Missing or invalid Authorization header"
        )
    
    token = auth_header.replace("Bearer ", "")
    
    try:
        supabase = get_supabase()
        supabase.auth.sign_out()
        
        return {"message": "Logged out successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    """
    Refresh access token using refresh token
    """
    try:
        supabase = get_supabase()
        
        response = supabase.auth.refresh_session(refresh_token)
        
        if not response.session:
            raise HTTPException(status_code=401, detail="Failed to refresh token")
        
        return {
            "access_token": response.session.access_token,
            "refresh_token": response.session.refresh_token,
            "expires_in": response.session.expires_in,
            "token_type": "bearer"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token refresh failed: {str(e)}")
