from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workspace import WorkSpace
from .crud_repo import CrudRepository
from ..models import WorkspaceMember
from ..core.exception import AppException
from sqlalchemy import select
from sqlalchemy.orm import selectinload

class WorkSpaceRepository(CrudRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkSpace,db)
        self.db = db

    async def create_member(self, workspace_member: WorkspaceMember):
        self.db.add(workspace_member)
        return workspace_member
    
    async def get_workspace_created_by_user(self, user_id: int, workspace_id: int | None = None):
        query = select(WorkSpace).where(WorkSpace.created_by == user_id)
        if workspace_id is not None:
            query = query.where(WorkSpace.id == workspace_id)
        if user_id is not None:
            query = query.where(WorkSpace.created_by == user_id)
        stmt = await self.db.execute(query.options(selectinload(WorkSpace.created_by_user)).execution_options(populate_existing=True))
        return stmt 
    
    async def get_workspace_by_profile(self, user_id: int):
        res = await self.get_workspace_created_by_user(user_id)
        return res.scalars().all()
    
    async def get_workspace_by_user(self, workspace_id: int, user_id: int):
        res = await self.get_workspace_created_by_user(user_id, workspace_id)
        return res.scalar_one_or_none()
    
    async def update_workspace(self, workspace_id: int, data: dict, current_user: int):
        res = await self.get_workspace_by_user(workspace_id, current_user)
        if res is None:
            raise AppException(message="No workspace found with this id for this user")
        for key, value in data.items():
            setattr(res, key, value)
        return res
    
    async def delete_workspace(self, workspace_id: int, user_id: int):
        res = await self.get_workspace_by_user(workspace_id, user_id)
        if res is None:
            raise AppException(message="No workspace found with this id for this user")
        await self.db.delete(res)
        return {"message": "Workspace deleted successfully"}

    async def get_members(self, workspace_id: int):
        res = await self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id
            ).options(selectinload(WorkspaceMember.user_workspace_member))
        )
        return res.scalars().all()
    
    async def get_member(self, workspace_id: int, user_id: int):
        res = await self.db.execute(
            select(WorkspaceMember).where(
                WorkspaceMember.workspace_id == workspace_id,
                WorkspaceMember.user_id == user_id
            ).options(selectinload(WorkspaceMember.user_workspace_member))
        )
        return res.scalar_one_or_none()
    
    async def delete_member(self,workspace_id,user_id):
        member = await self.get_member(workspace_id,user_id)
        if member is None:
            raise AppException(message="No member found with this workspace id and user id")
        await self.db.delete(member)
        return    {"message": "Member deleted successfully"}
