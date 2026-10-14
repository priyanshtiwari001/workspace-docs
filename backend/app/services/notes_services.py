from ..repositories import NotesRepository,WorkSpaceRepository
from ..models import Note
from ..core.exception import AppException
from sqlalchemy.orm import selectinload

class NotesService:
    def __init__(self, notes_repo: NotesRepository, workspace_repo: WorkSpaceRepository ):
        self.notes_repo = notes_repo
        self.workspace_repo = workspace_repo

    async def create_note(self, data,current_user):
        workspace_id = data.workspace_id
        is_exist = await self.workspace_repo.get(workspace_id)
        if not is_exist:
            raise AppException(f"No workspace found with this id {workspace_id}")
        if not current_user:
            raise AppException(f"No user found with this id {current_user}")
        new_notes = Note(
            title=data.title,
            content=data.content,
            author_id=current_user,
            workspace_id=int(data.workspace_id)
            
        )
        created_note =  await self.notes_repo.create(new_notes)
        result = await self.notes_repo.get(created_note.id,options=[selectinload(Note.author),selectinload(Note.workspace_note)],populate_existing=True)
        print("result",result)
        return result
    
    async def get_all_notes(self):
        return await self.notes_repo.get_all(options=[selectinload(Note.author),selectinload(Note.workspace_note)])
    
    async def get_note_by_id(self,id:int):
        res = await self.notes_repo.get(id,options=[selectinload(Note.author),selectinload(Note.workspace_note)],populate_existing=True)
        if res is None:
            raise AppException(f"No note found with this id {id}")
        return res
    
    async def update_notes(self,id,data:dict):
        is_note_exist = await self.notes_repo.get(id)

        if is_note_exist is None:
            raise AppException(f"No note found with this id {id}")
        
        await self.notes_repo.update(id,data)
        updated_res = await self.get_note_by_id(id)
        return updated_res

    async def delete_notes(self,id):
        is_note_exist = await self.notes_repo.get(id)
        if is_note_exist is None:
            raise AppException(f"No note found with this id {id}")
        return await self.notes_repo.delete(id)


