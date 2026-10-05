from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship, DeclarativeBase,Mapped,mapped_column
from base import Base
from user import User
from workspace import WorkSpace
from datetime import datetime,UTC

class Note(Base):
    __tablename__ = "notes"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    workspace_id: Mapped[int]=mapped_column(Integer,ForeignKey("workspaces.id"))
    author_id: Mapped[int]=mapped_column(Integer,ForeignKey("users.id"))
    title:Mapped[str] = mapped_column(String(150),nullable=False)
    content:Mapped[str] = mapped_column(String,nullable=False)
    created_at:Mapped[datetime] = mapped_column()
    updated_at:Mapped[datetime] = mapped_column()
    
    workspace: Mapped["WorkSpace"] = relationship(
        back_populates="notes"
    )
    author:Mapped["User"] = relationship(back_populates="user")
    