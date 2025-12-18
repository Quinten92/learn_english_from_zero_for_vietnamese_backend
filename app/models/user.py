"""
User Model
Example model for Learn English app
"""

from sqlalchemy import String, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column
from uuid import uuid4

from .base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """User model for learners"""
    
    __tablename__ = "users"
    
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid4())
    )
    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )
    full_name: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )
    avatar_url: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )
    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"
