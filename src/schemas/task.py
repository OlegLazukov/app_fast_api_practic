
from pydantic import BaseModel, Field, field_validator, UUID4
from typing import Optional
from datetime import datetime
from typing import List
from src.schemas.user import UserDB
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


class TaskResponse(BaseModel):
    id: UUID4
    title: str
    description: str
    author: UserDB
    observers: List[UserDB] = []
    column_id: UUID4 | None = None
    board_id: UUID4 | None = None
    sprint_id: UUID4 | None = None
    group_id: UUID4 | None = None
    status: TaskStatus
    created_at: datetime


class TaskListResponse(BaseModel):
    tasks: List[TaskResponse]