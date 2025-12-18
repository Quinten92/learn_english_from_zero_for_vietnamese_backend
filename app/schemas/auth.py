"""
Auth Schemas
Pydantic models for authentication requests and responses
"""

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    """Base user schema"""
    email: EmailStr
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None


class UserResponse(UserBase):
    """User response schema"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class TokenData(BaseModel):
    """Token payload data"""
    sub: str  # user id
    email: Optional[str] = None
    exp: Optional[int] = None


class AuthResponse(BaseModel):
    """Auth response with user info"""
    user: UserResponse
    message: str = "Authentication successful"


class GoogleAuthURL(BaseModel):
    """Google OAuth URL response"""
    url: str
    message: str = "Redirect to this URL to authenticate with Google"


class SessionResponse(BaseModel):
    """Session info response"""
    access_token: str
    refresh_token: str
    expires_in: int
    token_type: str = "bearer"
    user: UserResponse
