from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.preferences import Preferences
    from app.models.style_profile import StyleProfile
    from app.models.tweet import TweetHistory


class User(TimestampMixin, Base):
    """User model representing a vibe-tweet user."""

    __tablename__ = "users"

    username: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True,
    )
    email: Mapped[str | None] = mapped_column(
        String(255),
        unique=True,
        nullable=True,
    )

    # Relationships
    preferences: Mapped["Preferences | None"] = relationship(
        "Preferences",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )
    tweets: Mapped[list["TweetHistory"]] = relationship(
        "TweetHistory",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    style_profile: Mapped["StyleProfile | None"] = relationship(
        "StyleProfile",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, username={self.username})>"
