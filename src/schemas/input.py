from datetime import datetime

from pydantic import BaseModel, Field, field_validator, UUID4, EmailStr
from typing import List, Optional
from src.enums.task_status import TaskStatus



class TaskCreateRequest(BaseModel):
    title: str = Field(description="Заголовок задачи (не менее 3 символов)")
    description: str = Field(description="Описание задачи")
    author_id: UUID4
    observer_ids: Optional[List[UUID4]] = None
    assignee_id: UUID4 | None = None
    column_id: UUID4 | None = None
    board_id: UUID4 | None = None
    sprint_id: UUID4 | None = None
    group_id: UUID4 | None = None
    status: TaskStatus = Field(default=TaskStatus.todo)


    @field_validator('description')
    def validate_description(cls, v: str) -> str:
        if not v.strip():
            raise ValueError('Описание должно содержать хотя бы один символ')
        return v


    @field_validator('title')
    def validate_title(cls, v: str) -> str:
        if len(v) < 3:
            raise ValueError('Длина заголовка задачи должна быть не менее 3 символов')
        return v

class TaskUpdateRequest(BaseModel):
    title: Optional[str] = Field(None)
    description: Optional[str] = Field(None)
    observer_ids: Optional[List[UUID4]] = None
    status: Optional[TaskStatus] = None

    @field_validator('title')
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and len(v) < 3:
            raise ValueError('Длина заголовка задачи должна быть не менее 3 символов')
        return v

    @field_validator('description')
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        if v is not None and not v.strip():
            raise ValueError('Описание должно содержать хотя бы один символ')
        return v


class UserCreateRequest(BaseModel):
    full_name: str
    email: EmailStr

class UserUpdateRequest(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserFilters(BaseModel):
    full_name: Optional[str] = None
    email: Optional[str] = None


class BoardCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class BoardUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class GroupCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)

class GroupUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)



class SprintCreateRequest(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime

class SprintUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

class ColumnCreateRequest(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    board_id: UUID4 | None = None

class ColumnUpdateRequest(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    board_id: Optional[UUID4] = None