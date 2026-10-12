from app.repositories import workspace_repo
from ..repositories.workspace_repo import WorkSpaceRepository


class WorkSpaceService:
    def __init__(self, workspace_repo: WorkSpaceRepository) -> None:
        self.workspace_repo = workspace_repo

    async def create_workspace(self, name):
        workspace = await self.workspace_repo.create(name)
        return workspace

    async def get_workspaces(self, record_id):
        res = await self.workspace_repo.get(record_id)
        return res

    async def get_all_workspaces(self):
        res = await self.workspace_repo.get_all()
        return res
    

    async def update_workspace(self, record_id, data):
        res = await self.workspace_repo.update(record_id, data)
        return res

    async def delete_workspace(self, record_id):
        res = await self.workspace_repo.delete(record_id)
        return res