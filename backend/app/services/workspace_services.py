from app.repositories import workspace_repo
from ..core.exception import AppException
from ..repositories import WorkSpaceRepository,UserRepository
from ..models import WorkspaceMember,WorkSpace
from ..schemas.schemas import Roles
from sqlalchemy.orm import selectinload
class WorkSpaceService:
    def __init__(self, workspace_repo: WorkSpaceRepository,user_repo: UserRepository ) -> None:
        self.workspace_repo = workspace_repo
        self.user_repo = user_repo


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

    async def get_workspaces(self, record_id,user_id):
        workspace = await self.workspace_repo.get(record_id)
        if workspace is None:
            raise AppException(message="No workspace found with this id")
        user = await self.user_repo.get(user_id)
        if user is None:
            raise AppException(message="No user found with this id")
        res = await self.workspace_repo.get_workspace_by_user(record_id,user_id)
        return res

    async def get_all_workspaces(self):
        res = await self.workspace_repo.get_all(options=[selectinload(WorkSpace.created_by_user)],populate_existing=True)
        return res
    
    async def get_workspace_by_profile(self, user_id):
        res = await self.workspace_repo.get_workspace_by_profile(user_id)
        return res

    async def update_workspace(self, record_id,current_user, data):
        res = await self.workspace_repo.update_workspace(record_id, data, current_user)
        return res

    async def delete_workspace(self, record_id,user_id):
        res = await self.workspace_repo.delete_workspace(record_id,user_id)
        return res
    
    
    async def get_workspace_members(self, workspace_id):
        res = await self.workspace_repo.get_members(workspace_id)
        if res is None:
            return []
        return res
    
    async def get_workspace_member(self, workspace_id, user_id):
        workspace = await self.workspace_repo.get(workspace_id)
        if workspace is None:
            raise AppException(message="No workspace found with this id")
        user = await self.user_repo.get(user_id)
        if user is None:
            raise AppException(message="No user found with this id")
        res = await self.workspace_repo.get_member(workspace_id, user_id)
        if res is None:
            return AppException(message="No member found with this workspace id and user id")
        return res      
    
    async def change_member_role_in_workspace(self,workspace_id:int,user_id:int,role:Roles):
        workspace = await self.workspace_repo.get(workspace_id)
        if workspace is None:
            raise AppException(message="No workspace found with this id")
        user = await self.user_repo.get(user_id)
        if user is None:
            raise AppException(message="No user found with this id")
        existing_member = await self.workspace_repo.get_member(workspace_id, user_id)
        if existing_member is  None:
            raise   AppException(
        message="User is not a member of this workspace")
        existing_member.role = role
        return existing_member
    
    
    async def add_memeber_in_workspace(self,workspace_id:int,user_data):
         workspace = await self.workspace_repo.get(workspace_id)
         if workspace is None:
                    raise AppException(message="No workspace found with this id")
         user = await self.user_repo.get_user_by_email(user_data["email"])
         if user is None:
                    raise AppException(message="No user found with this id")
         exist_member = await self.workspace_repo.get_member(workspace_id,user.id)
         if exist_member:
             raise AppException(message="Member already exist in the workspace")
         
         new_member = WorkspaceMember(
             workspace_id=workspace_id,
             user_id=user.id
         )
         added_member =  await self.workspace_repo.create_member(new_member)
         return added_member
     
     
    async def delete_member(self,workspace_id:int,user_id:int):
         workspace = await self.workspace_repo.get(workspace_id)
         if workspace is None:
                    raise AppException(message="No workspace found with this id")
         user = await self.user_repo.get(user_id)
         if user is None:
                    raise AppException(message="No user found with this id")
         existing_member = await self.workspace_repo.get_member(workspace_id, user_id)
         if existing_member is  None:
             raise   AppException(
        message="User is not a member of this workspace")
         await self.workspace_repo.db.delete(existing_member)
         return {"message":"Member deleted successfully"}