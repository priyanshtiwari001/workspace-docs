from fastapi import APIRouter
from . import users, workspaces,notes,workspace_member

router = APIRouter(prefix="/api")


router.include_router(users.router, tags=["Users"])
router.include_router(workspaces.router, tags=["Workspaces"])
router.include_router(notes.router, tags=["Notes"])
router.include_router(workspace_member.router, tags=["Workspace Members"])