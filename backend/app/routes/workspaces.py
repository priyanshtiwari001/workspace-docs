from app.schemas.schemas import SuccessResponse
from fastapi import APIRouter, Depends
from ..schemas.schemas import WorkSpaceBase,WorkSpaceResponse
from ..core.databases import get_db
from typing import Annotated
from ..services import WorkSpaceService
from ..models import WorkSpace
from sqlalchemy.ext.asyncio import AsyncSession

from ..core.dependencies import get_workspace_service, get_current_user


router = APIRouter(prefix="/workspaces")


@router.post("",response_model=SuccessResponse[WorkSpaceResponse])
async def create_workspace(
    data: WorkSpaceBase,
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    new_workspace = WorkSpace(name=data.name, created_by=int(current_user))
    res = await workspace_service.create_workspace(new_workspace)
    await db.commit()
    await db.refresh(res,attribute_names=["created_by_user"])
    return SuccessResponse(data=res)



@router.get("/",response_model=SuccessResponse[list[WorkSpaceResponse]])
async def get_all_workspaces(
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await workspace_service.get_all_workspaces()
    await db.commit()
    # workspaces = WorkSpaceResponse.model_validate(res).model_dump()
    # await db.refresh(res)
    return SuccessResponse(data=res,message="Workspace fetched successfully")

@router.get("/profile",response_model=SuccessResponse[list[WorkSpaceResponse]])
async def get_workspace_by_profile(
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await workspace_service.get_workspace_by_profile(current_user)
    await db.commit()
    return SuccessResponse(data=res,message="Workspace fetched successfully")



@router.get("/{workspace_id}")
async def get_workspace(
    workspace_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await workspace_service.get_workspaces(workspace_id,current_user)
    await db.commit()
    await db.refresh(res)
    return res


@router.patch("/{workspace_id}")
async def update_workspace(
    workspace_id: int,
    data: WorkSpaceBase,
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await workspace_service.update_workspace(workspace_id, current_user, data.model_dump())
    await db.commit()
    return res


@router.delete("/{workspace_id}")
async def delete_workspace(
    workspace_id: int,
    db: Annotated[AsyncSession, Depends(get_db)],
    workspace_service: Annotated[WorkSpaceService, Depends(get_workspace_service)],
    current_user: Annotated[str, Depends(get_current_user)],
):
    res = await workspace_service.delete_workspace(workspace_id,current_user)
    await db.commit()
    return res
