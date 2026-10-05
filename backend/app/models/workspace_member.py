from sqlalchemy import  Integer, String, Text, ForeignKey,Boolean
from sqlalchemy.orm import relationship,Mapped,mapped_column
from base import Base
from note import Note
from workspace import WorkSpace
from datetime import datetime,UTC

class WorkspaceMembers(Base):
    __tablename__ = "workspace_members"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    workspace_id: Mapped[int] = mapped_column(Integer,ForeignKey("workspaces.id"),nullable=False)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    role: Mapped[str] = mapped_column(String(150),nullable=False)
    created_at:Mapped[datetime] = mapped_column()
    updated_at:Mapped[datetime] = mapped_column()
    
    
    
    
    

