from __future__ import annotations
from enum import Enum
from pydantic import BaseModel, EmailStr, ConfigDict, Field
from typing import Any, TypeVar, Generic

T = TypeVar("T")  # generic


class Roles(str, Enum):
    OWNER = "owner"
    VIEWER = "viewer"
    EDITOR = "editor"


class UserBase(BaseModel):
    email: EmailStr


class UserPrivate(UserBase):
    password: str


class BaseResponse(BaseModel):
    success: bool = True
    message: str = "Request completed successfully"
    error: Any = {}


class UserCreate(UserPrivate):
    password: str
    full_name: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    full_name: str
    model_config = ConfigDict(from_attributes=True)


class SuccessResponse(BaseResponse, Generic[T]):
    data: T
    model_config = ConfigDict(from_attributes=True)


class ErrorResponse(BaseModel):
    success: bool = False
    message: str = "Request is not completed successfully"
    data: dict = {}
    error: Any = {}


class TokenReponse(BaseModel):
    access_token: str
    token_type: str


class WorkSpaceBase(BaseModel):
    name: str = Field(min_length=1, max_length=50)
