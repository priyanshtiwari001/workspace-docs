from sqlalchemy.ext.asyncio import AsyncSession
from ..models import Note
from ..repositories import CrudRepository


class NotesRepository(CrudRepository):
    def __init__(self,  db: AsyncSession):
        super().__init__(Note, db)

   
        