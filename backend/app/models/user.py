from datetime import UTC, datetime

from backend.app.core.base import Base
from sqlalchemy import Boolean, Integer, String, DateTime,func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from workspace import WorkSpace
from refresh_token import RefreshToken
from workspace_member import WorkspaceMember


class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    email: Mapped[str] = mapped_column(String(150),nullable=False,unique=True)
    hashed_password : Mapped[str] = mapped_column(String(200),nullable=False)
    full_name: Mapped[str] = mapped_column(String(150),nullable=False)
    is_active:Mapped[bool] =  mapped_column(Boolean,nullable=False,default=False,server_default="False")
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    
    
    
    user_workspace:Mapped[list[WorkSpace]] = relationship(back_populates="created_by_user")
    user_workspace_members:Mapped[list[WorkspaceMember]] = relationship(back_populates="user")
    user_refresh_token:Mapped[list[RefreshToken]] = relationship(back_populates="user")
    

