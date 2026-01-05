import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class StyleProfile(Base):
    """
    Extracted writing style profile from user's tweet history.

    Profile structure:
    {
        "avg_length": 120,
        "vocabulary": {
            "common_words": ["the", "is", "tech"],
            "hashtag_frequency": 0.3,
            "mention_frequency": 0.1
        },
        "structure": {
            "avg_sentences": 2,
            "uses_threads": false,
            "uses_lists": false
        },
        "tone_markers": {
            "emoji_usage": 0.2,
            "humor_score": 0.5,
            "formality_score": 0.3
        },
        "themes": ["tech", "startups", "AI"]
    }
    """

    __tablename__ = "style_profiles"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # The extracted style profile
    profile: Mapped[dict] = mapped_column(
        JSONB,
        nullable=False,
    )

    # Number of tweets analyzed to generate this profile
    tweet_count: Mapped[int] = mapped_column(
        Integer,
        default=0,
        nullable=False,
    )

    # When the profile was last updated
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="style_profile")

    def __repr__(self) -> str:
        return f"<StyleProfile(user_id={self.user_id}, tweet_count={self.tweet_count})>"
