from datetime import datetime
from typing import TYPE_CHECKING

from ..core.base import Base
from sqlalchemy import DateTime, ForeignKey, Integer, String, func,Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from ..schemas.schemas import Roles as EnumRoles

if TYPE_CHECKING:
    from .user import User
    from .workspace import WorkSpace
class WorkspaceMember(Base):
    __tablename__ = "workspace_members"
    id:Mapped[int]=mapped_column(Integer,autoincrement=True,primary_key=True)
    workspace_id: Mapped[int] = mapped_column(Integer,ForeignKey("workspaces.id"),nullable=False)
    user_id : Mapped[int] = mapped_column(Integer,ForeignKey("users.id"),nullable=False)
    role: Mapped[EnumRoles] = mapped_column(SQLEnum(EnumRoles,name="user_role"),default=EnumRoles.VIEWER)
    created_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now())
    updated_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),nullable=False,server_default=func.now(),onupdate=func.now())
    

    workspace:Mapped["WorkSpace"] = relationship("WorkSpace",back_populates="workspace_members")
    user_workspace_member:Mapped["User"] = relationship("User", back_populates="user_workspace_members")
    
    
    
    
    
    

