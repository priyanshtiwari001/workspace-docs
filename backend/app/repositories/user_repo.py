from .crud_repo import CrudRepository
from ..models import User, RefreshToken
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select


class UserRepository(CrudRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(User, db)
        self.db = db

    async def get_user_by_email(self, email: str):
        user_email = await self.db.execute(select(User).where(User.email == email))
        return user_email.scalar_one_or_none()

    async def is_valid_refesh_token(self, token):
        res = await self.db.execute(
            select(RefreshToken).where(RefreshToken.token_hash == token)
        )
        return res

    async def create_refresh_token(self, refresh_token):
        self.db.add(refresh_token)
        await self.db.flush()
        await self.db.refresh(refresh_token)
