from fastapi import APIRouter, Depends
from ..schemas.schemas import NoteBase, SuccessResponse,NoteResponse,NoteCreate
from ..core.databases import get_db
from typing import Annotated
from ..services import NotesService
from ..core.dependencies import get_notes_service, get_current_user
from sqlalchemy.ext.asyncio import AsyncSession


router = APIRouter(prefix="/notes")



@router.post("/create",response_model=SuccessResponse[NoteResponse])
async def create_note(
    data: NoteCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    notes_service: Annotated[NotesService, Depends(get_notes_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await notes_service.create_note(data,current_user)
    await db.commit()
    notes = NoteResponse.model_validate(res).model_dump()
   
    return SuccessResponse(data=notes, message="Note created successfully")


@router.get("/",response_model=SuccessResponse[list[NoteResponse]])
async def get_all_notes(
    db: Annotated[AsyncSession, Depends(get_db)],
    notes_service: Annotated[NotesService, Depends(get_notes_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await notes_service.get_all_notes()
    await db.commit()
    return SuccessResponse(data=res, message="All Note created successfully")

@router.get("/{id}",response_model=SuccessResponse[NoteResponse])
async def get_note(
    id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    notes_service: Annotated[NotesService, Depends(get_notes_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await notes_service.get_note_by_id(id)
    await db.commit()
    return SuccessResponse(data=res, message="Note retrieved successfully")


@router.patch("/{id}")
async def update_note(
    id:int,
    db:Annotated[AsyncSession,Depends(get_db)],
    notes_service:Annotated[NotesService,Depends(get_notes_service)],
    current_user:Annotated[str,Depends(get_current_user)],
    data:NoteBase,
):  
    res = await notes_service.update_notes(id,data.model_dump())
    print("result",res)
    # await db.commit()
    notes = NoteResponse.model_validate(res).model_dump()
    return SuccessResponse(data=notes, message="Note updated successfully")



@router.delete("/{id}")
async def delete_note(
    id:int,
    db:Annotated[AsyncSession,Depends(get_db)],
    notes_service:Annotated[NotesService,Depends(get_notes_service)],
    current_user:Annotated[str,Depends(get_current_user)],
):
    res = await notes_service.delete_notes(id)
    await db.commit()
    return SuccessResponse(data=res, message="Note deleted successfully")