from fastapi import APIRouter
from . import users, workspaces

router = APIRouter(prefix="/api")


router.include_router(users.router, tags=["Users"])
router.include_router(workspaces.router, tags=["Workspaces"])
