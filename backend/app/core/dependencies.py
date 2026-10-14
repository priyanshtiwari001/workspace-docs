from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncSession
from ..core.databases import get_db
from ..repositories import WorkSpaceRepository, UserRepository,NotesRepository
from ..services import UserService, WorkSpaceService,NotesService
from fastapi import Depends, status
from typing import Annotated
from ..core.auth import oauth_schema, verify_jwt_token
from .exception import AppException



def get_workspace_repository(
    db: Annotated[AsyncSession, Depends(get_db)],
) -> WorkSpaceRepository:
    return WorkSpaceRepository(db)


def get_workspace_service(
    workspace_service: Annotated[
        WorkSpaceRepository, Depends(get_workspace_repository)
    ],
):
    return WorkSpaceService(workspace_service)


def get_notes_repository(db: Annotated[AsyncSession, Depends(get_db)]):
    return NotesRepository(db)
    

def get_user_repository(db: Annotated[AsyncSession, Depends(get_db)]) -> UserRepository:
    return UserRepository(db)


def get_user_service(
    user_repo: Annotated[UserRepository, Depends(get_user_repository)],
):
    return UserService(user_repo)

def get_notes_service(
    notes_repo: Annotated[NotesRepository, Depends(get_notes_repository)],
    workspace_repo: Annotated[WorkSpaceRepository, Depends(get_workspace_repository)],
):
    return NotesService(notes_repo, workspace_repo)



def get_current_user(token: Annotated[str, Depends(oauth_schema)]):
    print(token)
    user_id = verify_jwt_token(token)
    if not user_id:
        raise AppException(
            message="Not authenticated", status_code=status.HTTP_401_UNAUTHORIZED
        )

    return user_id
