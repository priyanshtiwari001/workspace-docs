from sqlalchemy import Column, Integer, String, Text, ForeignKey,DateTime,func
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship,Mapped,mapped_column
from ..core.base import Base
from datetime import datetime,UTC

if TYPE_CHECKING:
    from .user import User
    from .workspace import WorkSpace
class Note(Base):
    __tablename__ = "notes"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    workspace_id: Mapped[int]=mapped_column(Integer,ForeignKey("workspaces.id"))
    author_id: Mapped[int]=mapped_column(Integer,ForeignKey("users.id"))
    title:Mapped[str] = mapped_column(String(150),nullable=False)
    content:Mapped[str] = mapped_column(String,nullable=False)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    
    workspace_note: Mapped["WorkSpace"] = relationship(
        back_populates="notes",
    )
    author:Mapped["User"] = relationship("User",back_populates="user")
    