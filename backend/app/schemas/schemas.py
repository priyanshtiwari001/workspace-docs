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
    model_config = ConfigDict(from_attributes=True)

class WorkSpaceMemberBase(BaseModel):
    role:str
    model_config = ConfigDict(from_attributes=True)

class WorkSpaceResponse(WorkSpaceBase):
    id: int
    created_by_user:UserResponse
    # workspace_members:list[WorkSpaceMemberBase]
    model_config = ConfigDict(from_attributes=True)
    
class NoteBase(BaseModel):

    title: str = Field(min_length=1, max_length=50)
    content: str = Field(min_length=1, max_length=500)

    model_config = ConfigDict(from_attributes=True)

class NoteCreate(NoteBase):
    model_config = ConfigDict(from_attributes=True)

class NoteResponse(NoteBase):
    id: int | None = None
    workspace_note: WorkSpaceBase | None 
    author: UserResponse | None # if you different name use the this approach user: UserResponse = Field(validation_alias="author")
    model_config = ConfigDict(from_attributes=True)


