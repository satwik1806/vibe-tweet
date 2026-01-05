import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class TweetBase(BaseModel):
    """Base schema with shared tweet fields."""

    content: str = Field(..., min_length=1)
    tweet_id: str | None = None
    tweeted_at: datetime | None = None
    metadata: dict = Field(default_factory=dict)


class TweetCreate(TweetBase):
    """Schema for importing a single tweet."""

    pass


class TweetBulkImport(BaseModel):
    """Schema for bulk importing tweets."""

    tweets: list[TweetCreate]


class TweetResponse(TweetBase):
    """Schema for tweet responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime


class TweetImportResult(BaseModel):
    """Result of a bulk import operation."""

    imported: int
    skipped: int  # Duplicates or invalid
    total: int


class GeneratedTweet(BaseModel):
    """A generated tweet suggestion."""

    content: str
    confidence: float = Field(..., ge=0.0, le=1.0)
    trend_used: str | None = None
    tone_applied: str


class TweetGenerationRequest(BaseModel):
    """Request for generating tweet suggestions."""

    count: int = Field(default=5, ge=1, le=10)
    trends: list[str] | None = None  # Optional override for trends


class TweetGenerationResponse(BaseModel):
    """Response containing generated tweet suggestions."""

    suggestions: list[GeneratedTweet]
    style_profile_used: bool
    trends_used: list[str]
