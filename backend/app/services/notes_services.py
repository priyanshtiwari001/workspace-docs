from ..repositories import NotesRepository,WorkSpaceRepository
from ..models import Note
from ..core.exception import AppException
from sqlalchemy.orm import selectinload
from sqlalchemy import select

class NotesService:
    def __init__(self, notes_repo: NotesRepository, workspace_repo: WorkSpaceRepository ):
        self.notes_repo = notes_repo
        self.workspace_repo = workspace_repo

    async def create_note(self, data,current_user,workspace_id):
        is_exist = await self.workspace_repo.get(workspace_id)
        if not is_exist:
            raise AppException(f"No workspace found with this id {workspace_id}")
        if not current_user:
            raise AppException(f"No user found with this id {current_user}")
        new_notes = Note(
            title=data.title,
            content=data.content,
            author_id=current_user,
            workspace_id=int(workspace_id)
            
        )
        created_note =  await self.notes_repo.create(new_notes)
        result = await self.notes_repo.get(created_note.id,options=[selectinload(Note.author),selectinload(Note.workspace_note)],populate_existing=True)
        print("result",result)
        return result
    
    async def get_all_notes(self,workspace_id):
        is_exist = await self.workspace_repo.get(workspace_id)
        if not is_exist:
            raise AppException(f"No workspace found with this id {workspace_id}")
        
        res = await self.notes_repo.db.execute(select(Note).options(selectinload(Note.author),selectinload(Note.workspace_note)).where(Note.workspace_id==workspace_id).execution_options(populate_existing=True))
        notes = res.scalars().all()
        return notes
    
    async def get_note_by_id(self,id:int,workspace_id:int):
        is_exist = await self.workspace_repo.get(workspace_id)
        if not is_exist:
            raise AppException(f"No workspace found with this id {workspace_id}")
        res = await self.notes_repo.db.execute(select(Note).options(selectinload(Note.author),selectinload(Note.workspace_note)).where(Note.workspace_id==workspace_id,Note.id==id))
        notes = res.scalars().first()
        
        if notes is None:
            raise AppException(f"No note found with this id {id} in this workspace")
        return notes
    
    async def update_notes(self,id,data:dict,workspace_id):
        is_workspace_exist = await self.workspace_repo.get(workspace_id)

        if is_workspace_exist is None:
            raise AppException(f"No note or workspace found with this id {id}")
        
        res =  await self.notes_repo.db.execute(select(Note).options(selectinload(Note.author),selectinload(Note.workspace_note)).where(Note.workspace_id==workspace_id,Note.id==id).execution_options(populate_existing=True))
        note = res.scalar_one_or_none()
        if note is None:
            raise AppException(f"No note found with this id {id} in this workspace")
        if data.get("title") is not None:
            note.title = data["title"]
        if data.get("content") is not None:            
            note.content = data["content"]
        return note

    async def delete_notes(self,id,workspace_id):
        is_note_exist = await self.notes_repo.db.execute(select(Note).options(selectinload(Note.author),selectinload(Note.workspace_note)).where(Note.workspace_id==workspace_id,Note.id==id))
        note = is_note_exist.scalar_one_or_none()
        if note is None:
            raise AppException(f"No note found with this id {id} in this workspace")
        is_workspace_exist = await self.workspace_repo.get(workspace_id)
        if is_workspace_exist is None:
            raise AppException(f"No workspace found with this id {workspace_id}")
        return await self.notes_repo.delete(id)


