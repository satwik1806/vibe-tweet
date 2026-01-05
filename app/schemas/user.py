import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UserBase(BaseModel):
    """Base schema with shared user fields."""

    username: str = Field(..., min_length=1, max_length=50)


class UserCreate(UserBase):
    """Schema for creating a new user."""

    email: EmailStr | None = None


class UserUpdate(BaseModel):
    """Schema for updating a user."""

    username: str | None = Field(None, min_length=1, max_length=50)
    email: EmailStr | None = None


class UserResponse(UserBase):
    """Schema for user responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    email: str | None
    created_at: datetime
    updated_at: datetime


class UserWithPreferences(UserResponse):
    """User response including preferences."""

    from app.schemas.preferences import PreferencesResponse

    preferences: "PreferencesResponse | None" = None
