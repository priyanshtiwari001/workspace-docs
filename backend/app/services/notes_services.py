from ..repositories import NotesRepository,WorkSpaceRepository
from ..models import Note
from ..core.exception import AppException

class NotesService:
    def __init__(self, notes_repo: NotesRepository, workspace_repo: WorkSpaceRepository ):
        self.notes_repo = notes_repo
        self.workspace_repo = workspace_repo

    async def create_note(self, data,current_user):
        workspace_id = data.workspace_id
        is_exist = await self.workspace_repo.get(workspace_id)
        if not is_exist:
            raise AppException(f"No workspace found with this id {workspace_id}")
        new_notes = Note(
            title=data.title,
            content=data.content,
            author_id=current_user,
            workspace_id=int(data.workspace_id)
            
        )
        note = await self.notes_repo.create(new_notes)
        return note

    