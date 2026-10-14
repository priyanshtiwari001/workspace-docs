from fastapi import APIRouter, Depends
from ..schemas.schemas import NoteBase, SuccessResponse,NoteResponse
from ..core.databases import get_db
from typing import Annotated
from ..services import NotesService
from ..core.dependencies import get_notes_service, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/notes")



@router.post("/create",)
async def create_note(
    data: NoteBase,
    db: Annotated[AsyncSession, Depends(get_db)],
    notes_service: Annotated[NotesService, Depends(get_notes_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await notes_service.create_note(data,current_user)
    await db.commit()
    await db.refresh(res,attribute_names=["workspace_note","author"])
    notes = NoteResponse.validate(res).model_dump()
    return SuccessResponse(data=notes, message="Note created successfully")
