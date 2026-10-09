from datetime import datetime

from backend.app.core.base import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, func,Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from user import User



class RefreshToken(Base):
    __tablename__ = "refresh_tokens"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    token_hash: Mapped[str] = mapped_column(String(200))
    revoked_at:Mapped[datetime]= mapped_column(DateTime(timezone=True))
    expired_at :Mapped[datetime]= mapped_column(DateTime(timezone=True))
    
    user:Mapped[User]=relationship(back_populates="user_refresh_token")
