from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ..core.base import Base

if TYPE_CHECKING:
    from .user import User


class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id: Mapped[int] = mapped_column(Integer, autoincrement=True, primary_key=True)
    user_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=False
    )
    token_hash: Mapped[str] = mapped_column(String(200))
    revoked_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    expired_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    user_refresh_tokens: Mapped[User] = relationship(
        "User",
        back_populates="refresh_tokens",
    )
