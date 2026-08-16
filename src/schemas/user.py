from pydantic import BaseModel, Field, field_validator, UUID4, EmailStr
from typing import List, Optional


class UserCreateRequest(BaseModel):
    full_name: str
    email: EmailStr

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserFilters(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class UserDB(BaseModel):
    id: UUID4
    full_name: str
    email: str


class CreateUserResponse(BaseModel):
    payload: UserDB

class UserResponse(BaseModel):
    payload: UserDB | None

class UsersListResponse(BaseModel):
    payload: List[UserDB]