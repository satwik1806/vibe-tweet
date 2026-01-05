import uuid
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.user import User


class Preferences(TimestampMixin, Base):
    """User preferences for tweet generation."""

    __tablename__ = "preferences"

    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        unique=True,
        nullable=False,
        index=True,
    )

    # List of interest topics (e.g., ["tech", "startups", "AI"])
    interests: Mapped[list] = mapped_column(
        JSONB,
        default=list,
        nullable=False,
    )

    # Preferred tone: casual, sarcastic, serious, humorous, controversial, informative
    tone: Mapped[str] = mapped_column(
        String(50),
        default="casual",
        nullable=False,
    )

    # LLM provider preference: "claude" or "openai"
    llm_provider: Mapped[str] = mapped_column(
        String(20),
        default="claude",
        nullable=False,
    )

    # Relationship
    user: Mapped["User"] = relationship("User", back_populates="preferences")

    def __repr__(self) -> str:
        return f"<Preferences(user_id={self.user_id}, tone={self.tone})>"
