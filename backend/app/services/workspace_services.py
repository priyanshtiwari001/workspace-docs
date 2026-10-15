from app.repositories import workspace_repo
from ..repositories.workspace_repo import WorkSpaceRepository
from ..models import WorkspaceMember,WorkSpace
from ..schemas.schemas import Roles
from sqlalchemy.orm import selectinload
class WorkSpaceService:
    def __init__(self, workspace_repo: WorkSpaceRepository) -> None:
        self.workspace_repo = workspace_repo

    async def create_workspace(self, name):
        workspace = await self.workspace_repo.create(name)

        workspace_member = WorkspaceMember(
            workspace_id=workspace.id,
            user_id=workspace.created_by,
            role=Roles.OWNER.value
        )
        print("workspace_member", workspace_member)
        await self.workspace_repo.create_member(workspace_member)
        return workspace

    async def get_workspaces(self, record_id):
        res = await self.workspace_repo.get(record_id)
        return res

    async def get_all_workspaces(self):
        res = await self.workspace_repo.get_all(options=[selectinload(WorkSpace.created_by_user)],populate_existing=True)
        return res
    

    async def update_workspace(self, record_id, data):
        res = await self.workspace_repo.update(record_id, data)
        return res

    async def delete_workspace(self, record_id):
        res = await self.workspace_repo.delete(record_id)
        return res