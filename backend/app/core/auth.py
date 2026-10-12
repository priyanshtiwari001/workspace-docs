from pwdlib import PasswordHash
import jwt
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from fastapi import status
from datetime import datetime, timedelta, UTC
from .config import settings
from .exception import AppException
import string
import secrets

oauth_schema = OAuth2PasswordBearer(tokenUrl="/api/users/login")
# oauth_schema = HTTPBearer()

password_hash = PasswordHash.recommended()


def hash_password(plain_pwd: str) -> str:
    return password_hash.hash(plain_pwd)


def verify_hash_password(plain_pwd: str, hash_pwd: str) -> bool:
    return password_hash.verify(plain_pwd, hash_pwd)


def create_jwt_token(payload: dict, expire_time):
    """Create jwt token"""
    to_encode = payload.copy()
    expire = datetime.now(UTC) + timedelta(minutes=expire_time)
    to_encode["exp"] = expire
    token = jwt.encode(
        to_encode, settings.secret_key.get_secret_value(), settings.algorithm
    )
    return token


def verify_jwt_token(token: str):
    try:
        payload = jwt.decode(
            token,
            settings.secret_key.get_secret_value(),
            algorithms=[settings.algorithm],
        )
    except jwt.ExpiredSignatureError as e:
        raise AppException(
            message="Token is expired!",
            explanation=str(e),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    except jwt.DecodeError as e:
        raise AppException(
            message="Token cannot be decoded because it failed validation!",
            explanation=str(e),
            status_code=status.HTTP_401_UNAUTHORIZED,
        )

    return payload.get("sub")


def generate_secure_random_string(length: int = 64) -> str:
    alphabet = string.ascii_letters + string.digits
    return "".join(secrets.choice(alphabet) for _ in range(length))
