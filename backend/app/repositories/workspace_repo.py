from sqlalchemy.ext.asyncio import AsyncSession
from ..models.workspace import WorkSpace
from .crud_repo import CrudRepository


class WorkSpaceRepository(CrudRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(WorkSpace,db)
        self.db = db