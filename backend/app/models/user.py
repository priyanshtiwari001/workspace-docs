from sqlalchemy import Column, Integer, String, Text, ForeignKey,Boolean
from sqlalchemy.orm import relationship,Mapped,mapped_column
from base import Base
from note import Note
from workspace import WorkSpace
from datetime import datetime,UTC

class User(Base):
    __tablename__ = "users"
    
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    email: Mapped[str] = mapped_column(String(150),nullable=False,unique=True)
    hashed_password : Mapped[str] = mapped_column(String(200),nullable=False)
    full_name: Mapped[str] = mapped_column(String(150),nullable=False)
    is_active:Mapped[bool] =  mapped_column(Boolean,nullable=False,default=False,server_default="False")
    created_at:Mapped[datetime] = mapped_column()
    updated_at:Mapped[datetime] = mapped_column()
    
    
    
    user_workspace:Mapped[list["WorkSpace"]] = relationship(back_populates="created_by_user")
    

