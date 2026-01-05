import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class VocabularyProfile(BaseModel):
    """Vocabulary analysis results."""

    common_words: list[str] = Field(default_factory=list)
    hashtag_frequency: float = Field(default=0.0, ge=0.0, le=1.0)
    mention_frequency: float = Field(default=0.0, ge=0.0, le=1.0)


class StructureProfile(BaseModel):
    """Tweet structure analysis results."""

    avg_sentences: float = Field(default=1.0, ge=0.0)
    uses_threads: bool = False
    uses_lists: bool = False


class ToneMarkers(BaseModel):
    """Tone and style markers."""

    emoji_usage: float = Field(default=0.0, ge=0.0, le=1.0)
    humor_score: float = Field(default=0.0, ge=0.0, le=1.0)
    formality_score: float = Field(default=0.5, ge=0.0, le=1.0)


class StyleProfileData(BaseModel):
    """The full style profile structure."""

    avg_length: float = Field(default=0.0, ge=0.0)
    vocabulary: VocabularyProfile = Field(default_factory=VocabularyProfile)
    structure: StructureProfile = Field(default_factory=StructureProfile)
    tone_markers: ToneMarkers = Field(default_factory=ToneMarkers)
    themes: list[str] = Field(default_factory=list)


class StyleProfileResponse(BaseModel):
    """Schema for style profile responses."""

    model_config = ConfigDict(from_attributes=True)

    id: uuid.UUID
    user_id: uuid.UUID
    profile: StyleProfileData
    tweet_count: int
    updated_at: datetime


class StyleProfileSummary(BaseModel):
    """Simplified summary of a user's style."""

    has_profile: bool
    tweet_count: int = 0
    top_themes: list[str] = Field(default_factory=list)
    avg_tweet_length: float = 0.0
    emoji_usage: str = "none"  # none, low, medium, high
    humor_level: str = "neutral"  # serious, neutral, playful, very_playful
