import uuid
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

# Valid tone options
ToneType = Literal["casual", "sarcastic", "serious", "humorous", "controversial", "informative"]

# Valid LLM provider options
LLMProviderType = Literal["claude", "openai"]


class PreferencesBase(BaseModel):
    """Base schema with shared preferences fields."""

    interests: list[str] = Field(default_factory=list)
    tone: ToneType = "casual"
    llm_provider: LLMProviderType = "claude"


class PreferencesCreate(PreferencesBase):
    """Schema for creating preferences (usually auto-created with user)."""

    pass


class PreferencesUpdate(BaseModel):
    """Schema for updating preferences."""

    interests: list[str] | None = None
    tone: ToneType | None = None
    llm_provider: LLMProviderType | None = None


class PreferencesResponse(PreferencesBase):
    """Schema for preferences responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
