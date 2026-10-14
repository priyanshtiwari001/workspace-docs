from fastapi import APIRouter
from . import users, workspaces,notes

router = APIRouter(prefix="/api")


router.include_router(users.router, tags=["Users"])
router.include_router(workspaces.router, tags=["Workspaces"])
router.include_router(notes.router, tags=["Notes"])
