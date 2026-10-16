from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String, Text, ForeignKey,DateTime,func
from sqlalchemy.orm import relationship,Mapped,mapped_column
from ..core.base import Base
from datetime import datetime,UTC

if TYPE_CHECKING:
    from .workspace_member import WorkspaceMember
    from .user import User
    from .note import Note

class WorkSpace(Base):
    __tablename__ = "workspaces"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    name: Mapped[str] = mapped_column(String(150),nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    
    notes:Mapped[list["Note"]] = relationship("Note", back_populates="workspace_note")
    created_by_user:Mapped["User"] = relationship("User", back_populates="user_workspace")
    workspace_members: Mapped[list["WorkspaceMember"]] = relationship(
    "WorkspaceMember",
    back_populates="workspace",
     cascade="all, delete-orphan",
    )
    
    
    def __abs__(self):
        return f"WorkSpace(id={self.id}, name={self.name}, created_by={self.created_by})"
