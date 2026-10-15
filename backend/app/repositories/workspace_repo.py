from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workspace import WorkSpace
from .crud_repo import CrudRepository
from ..models import WorkspaceMember


class WorkSpaceRepository(CrudRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkSpace,db)
        self.db = db

    async def create_member(self, workspace_member: WorkspaceMember):
        self.db.add(workspace_member)
        return workspace_member
    