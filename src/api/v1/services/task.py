
from typing import List, Sequence
from fastapi import HTTPException
from pydantic import UUID4
from src.repositories import TaskRepository
from src.schemas.task import TaskCreateRequest, TaskUpdateRequest, TaskResponse, TaskListResponse
from src.models.models import Task, User
from src.utils.constants import TASK_EXIST_MSG, TASK_NOT_FOUND_MSG, TASK_FAIL_MSG, AUTHOR_NOT_FOUND_MSG, USER_NOT_FOUND_MSG
from src.utils.service import BaseService, transaction_mode


class TaskService(BaseService, TaskRepository):
    _repo: str = "task"

    @transaction_mode(auto_flush=True)
    async def create_task(self, task_data: TaskCreateRequest) -> TaskResponse:
        existing_task = await self.uow.task.get_by_name(title=task_data.title)
        if existing_task:
            raise HTTPException(status_code=409, detail=TASK_EXIST_MSG)

        task_data_dict = task_data.model_dump(exclude_unset=True, exclude={'observer_ids'})

        new_task_sa: Task = await self.add_one_and_get_obj(**task_data_dict)

        if task_data.observer_ids:
            observers = await self._get_users_by_ids(task_data.observer_ids)
            new_task_sa.observers.extend(observers)


        task_with_relations = await self.uow.task.get_with_relations(new_task_sa.id)
        if not task_with_relations:
            raise HTTPException(status_code=500, detail=TASK_FAIL_MSG)

        return task_with_relations.to_task_response_schema()

    @transaction_mode
    async def get_task(self, task_id: UUID4) -> TaskResponse | None:
        task_sa = await self.uow.task.get_with_relations(task_id)
        self.check_existence(task_sa, details=TASK_NOT_FOUND_MSG)
        return task_sa.to_task_response_schema()

    @transaction_mode
    async def get_all_tasks(self, author_id: UUID4 | None = None, status: str | None = None) -> TaskListResponse:
        tasks_sa = await self.uow.task.get_all_with_relations()
        filtered_tasks = []
        for task in tasks_sa:
            if author_id is not None and task.author_id != author_id:
                continue
            if status is not None and str(task.status.value) != status:
                continue
            filtered_tasks.append(task)
        return TaskListResponse(tasks=[task.to_task_response_schema() for task in filtered_tasks])

    @transaction_mode(auto_flush=True)
    async def update_task(self, task_id: UUID4, task_data: TaskUpdateRequest) -> TaskResponse | None:
        existing_task_sa = await self.uow.task.get_with_relations(task_id)
        self.check_existence(existing_task_sa, details=TASK_NOT_FOUND_MSG)

        update_data = task_data.model_dump(exclude_unset=True)

        fields_to_update = {k: v for k, v in update_data.items() if
                            k not in ['author_id', 'executor_id', 'observer_ids']}

        await self.update_one_by_id(obj_id=task_id, **fields_to_update)

        if 'author_id' in update_data:
            if update_data['author_id'] is not None:
                new_author = await self.get_by_filter_one_or_none(update_data['author_id'])
                if not new_author:
                    raise HTTPException(status_code=400, detail=AUTHOR_NOT_FOUND_MSG)
                existing_task_sa.author = new_author
            else:
                existing_task_sa.author = None


        if 'observer_ids' in update_data:
            existing_task_sa.observers.clear()
            if update_data['observer_ids']:
                new_observers = await self._get_users_by_ids(update_data['observer_ids'])
                existing_task_sa.observers.extend(new_observers)

        await self.uow.refresh(existing_task_sa)

        task_with_relations = await self.uow.task.get_with_relations(existing_task_sa)
        if not task_with_relations:
            raise HTTPException(status_code=500, detail=TASK_FAIL_MSG)

        return task_with_relations.to_task_response_schema()

    @transaction_mode
    async def delete_task(self, task_id: UUID4) -> None:
        existing_task = await self.get_by_filter_one_or_none(id=task_id)
        self.check_existence(existing_task, details=TASK_NOT_FOUND_MSG)

        await self.delete_by_ids(task_id)

    @transaction_mode
    async def _get_users_by_ids(self, user_ids: List[UUID4]) -> Sequence[User]:
        unique_ids = list(set(user_ids))
        users = await self.uow.user.get_by_ids(ids=unique_ids)
        if len(users) != len(user_ids):
            found_ids = {user.id for user in users}
            missing_ids = [str(uid) for uid in user_ids if uid not in found_ids]
            raise HTTPException(status_code=400, detail=f"User not found {', '.join(missing_ids)}")
        return users
