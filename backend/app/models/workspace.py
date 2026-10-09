from sqlalchemy import Column, Integer, String, Text, ForeignKey,DateTime,func
from sqlalchemy.orm import relationship,Mapped,mapped_column
from backend.app.core.base import Base
from note import Note
from user import User
from datetime import datetime,UTC

class WorkSpace(Base):
    __tablename__ = "workspaces"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    name: Mapped[str] = mapped_column(String(150),nullable=False)
    created_by: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    
    notes:Mapped[list["Note"]] = relationship(back_populates="workspace")
    created_by_user:Mapped["User"] = relationship(back_populates="user_workspace")
