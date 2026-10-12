from fastapi import APIRouter, Depends, status, Response, Request
from typing import Annotated

from sqlalchemy.ext.asyncio import AsyncSession
from ..services.user_services import UserService
from ..schemas.schemas import (
    SuccessResponse,
    UserCreate,
    UserResponse,
    TokenReponse,
)
from ..core.databases import get_db
from ..core.dependencies import get_user_service, get_current_user
from fastapi.security import OAuth2PasswordRequestForm
from ..models import RefreshToken
from sqlalchemy import select
from datetime import datetime, UTC
from ..core.exception import AppException

router = APIRouter(prefix="/users")


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=SuccessResponse[UserResponse],
)
async def create_user(
    user: UserCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    new_user = await user_service.create_user(user)
    await db.commit()  # Commit the transaction to persist changes in the database
    # user_response = UserResponse.model_validate(new_user)
    return SuccessResponse(message="User created successfully", data=new_user)


@router.post("/login")
async def login(
    response: Response,
    user_data: Annotated[dict, Depends(OAuth2PasswordRequestForm)],
    db: Annotated[AsyncSession, Depends(get_db)],
    user_repo: Annotated[UserService, Depends(get_user_service)],
):

    user_token = await user_repo.login_user(user_data, response)
    await db.commit()

    token = {"access_token": user_token, "token_type": "bearer"}
    return token


@router.get("")
async def get_my_profile(
    current_user: Annotated[str, Depends(get_current_user)],
    user_repo: Annotated[UserService, Depends(get_user_service)],
):
    print(current_user)
    user_data = await user_repo.my_profile(current_user)
    return user_data


@router.get("/all", response_model=SuccessResponse[list[UserResponse]])
async def get_all_users(
    current_user: Annotated[str, Depends(get_current_user)],
    user_repo: Annotated[UserService, Depends(get_user_service)],
):
    users = await user_repo.get_all_users()
    return SuccessResponse(data=users)


# @router.post("/refresh")
# async def get_new_access_token(
#     request: Request, db: Annotated[AsyncSession, Depends(get_db)]
# ):
#     raw_refresh_token = request.cookies.get("refresh_token")
#     print("raw token", raw_refresh_token)

#     db_token = await db.execute(
#         select(RefreshToken).where(
#             RefreshToken.token_hash == raw_refresh_token,
#             RefreshToken.revoked_at.is_(None),
#             RefreshToken.expired_at > datetime.now(UTC),
#         )
#     )
#     token = db_token.scalar_one_or_none()

#     if not token:
#         raise AppException(message="Invalid or revoked refresh token")

#     token.revoked_at = datetime.now()


# Pseudo-code for Refresh
# @app.post("/user/refresh")
# async def get_new_access_token(request, db):
#     # 1. Read the raw refresh token from the HttpOnly cookie
#     raw_refresh_token = request.cookies.get("refresh_token")
#     if not raw_refresh_token:
#         raise HTTPException(401, "No refresh token provided")

#     # 2. Hash the incoming token to compare with DB
#     incoming_hash = hash_with_sha256(raw_refresh_token)

#     # 3. Look up the hash in the DB. It must be valid (not revoked, not expired)
#     db_token = db.query(RefreshToken).filter(
#         RefreshToken.token_hash == incoming_hash,
#         RefreshToken.revoked_at.is_(None),
#         RefreshToken.expires_at > datetime.now()
#     ).first()

#     # 4. SECURITY ALERT: If not found, someone is using a stolen/revoked token!
#     if not db_token:
#         raise HTTPException(403, "Invalid or revoked refresh token")

#     # --- REFRESH TOKEN ROTATION (Optional but highly recommended) ---
#     # 5. Revoke the old token
#     db_token.revoked_at = datetime.now()

#     # 6. Generate a brand new refresh token for the user
#     new_raw_token = generate_secure_random_string()
#     new_hashed_token = hash_with_sha256(new_raw_token)
#     db.add(RefreshToken(user_id=db_token.user_id, token_hash=new_hashed_token, expires_at=...))
#     await db.commit()

#     # 7. Fetch the user's LATEST roles from DB (Solves the stale JWT problem!)
#     roles = get_user_roles(db_token.user_id)

#     # 8. Create a NEW 15-minute access token with updated roles
#     new_access_token = create_jwt_token({"sub": str(db_token.user_id), "roles": roles}, 15)

#     # 9. Set the NEW refresh token in the cookie
#     response.set_cookie(key="refresh_token", value=new_raw_token, httponly=True)

#     # 10. Return the new access token to the frontend
#     return {"access_token": new_access_token, "token_type": "bearer"}
