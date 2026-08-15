from datetime import datetime

from pydantic import BaseModel, UUID4, ConfigDict
from typing import List

from uvicorn.config import Config

from src.enums.task_status import TaskStatus


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


class BoardResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class GroupResponse(BaseModel):
    name: str
    model_config = ConfigDict(from_attributes=True)

class SprintResponse(BaseModel):
    name: str
    start_date: datetime
    end_date: datetime
    model_config = ConfigDict(from_attributes=True)

class ColumnResponse(BaseModel):
    name: str
    board_id: UUID4 | None = None
    model_config = ConfigDict(from_attributes=True)

class BoardListResponse(BaseModel):
    boards: List[BoardResponse]

class GroupListResponse(BaseModel):
    groups: List[GroupResponse]


class SprintListResponse(BaseModel):
    sprints: List[SprintResponse]

class ColumnListResponse(BaseModel):
    columns: List[ColumnResponse]