import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class TweetHistory(Base):
    """Historical tweets imported from user's Twitter/X account."""

    __tablename__ = "tweet_history"

    id: Mapped[uuid.UUID] = mapped_column(
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # Tweet content
    content: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # Original Twitter/X tweet ID (for deduplication)
    tweet_id: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        unique=True,
    )

    # Original tweet timestamp
    tweeted_at: Mapped[datetime | None] = mapped_column(
        nullable=True,
    )

    # Metadata: likes, retweets, replies, etc.
    metadata: Mapped[dict] = mapped_column(
        JSONB,
        default=dict,
        nullable=False,
    )

    # When this record was imported
    created_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="tweets")

    def __repr__(self) -> str:
        preview = self.content[:30] + "..." if len(self.content) > 30 else self.content
        return f"<TweetHistory(id={self.id}, content='{preview}')>"
