from typing import Annotated

from app.schemas.schemas import SuccessResponse
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.databases import get_db
from ..core.dependencies import get_current_user, get_workspace_service
from ..schemas.schemas import WorkSpaceMemberResponse,Roles,UserBase
from ..services import WorkSpaceService

router = APIRouter(prefix="/workspaces/{workspace_id}/members")

@router.get("",response_model=SuccessResponse[list[WorkSpaceMemberResponse]])
async def get_workspace_members(
    workspace_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[str, Depends(get_current_user)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
):
    res = await workspace_service.get_workspace_members(workspace_id)
    await db.commit()
    return SuccessResponse(data=res, message="Workspace members fetched successfully")


@router.get("/{member_id}",response_model=SuccessResponse[WorkSpaceMemberResponse])
async def get_workspace_member(
    workspace_id: int,
    member_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[str, Depends(get_current_user)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
):
    res = await workspace_service.get_workspace_member(workspace_id, member_id)
    await db.commit()
    return SuccessResponse(data=res, message="Workspace member fetched successfully")


@router.patch("/{member_id}")
async def change_role_to_member(
     workspace_id: int,
    member_id: int,
    role:Roles,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[str, Depends(get_current_user)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
):
    res = await workspace_service.change_member_role_in_workspace(workspace_id,member_id,role)
    await db.commit()
    return res


@router.post("/add_member")
async def add_member_in_workspace(
     workspace_id: int,
        user_data:UserBase,
        db: Annotated[AsyncSession, Depends(get_db)],
        current_user: Annotated[str, Depends(get_current_user)],
        workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
):
    res = await workspace_service.add_memeber_in_workspace(workspace_id,user_data.model_dump())
    await db.commit()
    return res


@router.delete("")
async def delete_member(
      workspace_id: int,
      member_id: int,
       db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[str, Depends(get_current_user)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
):
    res = await workspace_service.delete_member(workspace_id,member_id)
    await db.commit()
    return res