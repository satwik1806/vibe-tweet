"""Pydantic schemas for vibe-tweet API."""

from app.schemas.preferences import (
    PreferencesCreate,
    PreferencesResponse,
    PreferencesUpdate,
)
from app.schemas.style_profile import (
    StyleProfileData,
    StyleProfileResponse,
    StyleProfileSummary,
)
from app.schemas.tweet import (
    GeneratedTweet,
    TweetBulkImport,
    TweetCreate,
    TweetGenerationRequest,
    TweetGenerationResponse,
    TweetImportResult,
    TweetResponse,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserWithPreferences,
)

__all__ = [
    # User
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserWithPreferences",
    # Preferences
    "PreferencesCreate",
    "PreferencesUpdate",
    "PreferencesResponse",
    # Tweet
    "TweetCreate",
    "TweetBulkImport",
    "TweetResponse",
    "TweetImportResult",
    "GeneratedTweet",
    "TweetGenerationRequest",
    "TweetGenerationResponse",
    # Style Profile
    "StyleProfileData",
    "StyleProfileResponse",
    "StyleProfileSummary",
]
