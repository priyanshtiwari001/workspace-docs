from ..repositories.user_repo import UserRepository
from fastapi import status, Response
from ..core.exception import AppException
from ..models import User, RefreshToken
from ..core.auth import (
    hash_password,
    verify_hash_password,
    create_jwt_token,
    generate_secure_random_string,
)
from ..core.config import settings
from datetime import datetime, UTC, timedelta


class UserService:
    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    async def create_user(self, user_data):
        existing_user = await self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise AppException(
                message="User with this email already exists.",
                status_code=status.HTTP_400_BAD_REQUEST,
            )

        new_user = User(
            full_name=user_data.full_name,
            email=user_data.email,
            hashed_password=hash_password(user_data.password),
        )

        user = await self.user_repo.create(new_user)
        return user

    async def login_user(self, user_data, response: Response):
        exist_user = await self.user_repo.get_user_by_email(user_data.username)
        if not exist_user or not verify_hash_password(
            user_data.password, exist_user.hashed_password
        ):
            raise AppException(
                message="email or password is incorrect or mismatched!",
                status_code=status.HTTP_409_CONFLICT,
            )
        user_id = exist_user.id
        token = create_jwt_token({"sub": str(user_id)}, settings.expire_time_in_mins)

        # refresh token
        raw_refresh_token = generate_secure_random_string()

        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=raw_refresh_token,
            expired_at=datetime.now(UTC)
            + timedelta(days=settings.refresh_token_duration_in_days),
            revoked_at=None,
        )
        await self.user_repo.create_refresh_token(refresh_token)

        response.set_cookie(
            key="refresh_token",
            value=raw_refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        return token

    async def my_profile(self, current_user_id):
        user = await self.user_repo.get(current_user_id)
        return user

    async def get_all_users(self):
        res = await self.user_repo.get_all()
        return res
