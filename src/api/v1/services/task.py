
from typing import List, Sequence

from fastapi import Depends, HTTPException
from pydantic import UUID4

from sqlalchemy.future import select
from src.schemas.input import TaskCreateRequest, TaskUpdateRequest
from src.schemas.output import TaskResponse, UserDB, TaskListResponse
from src.models.models import Task, User
from src.utils.unit_of_work import UnitOfWork


class TaskService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    def _user_to_userdb(self, user_sa: User | None) -> UserDB | None:
        if not user_sa:
            return None
        return UserDB(
            id=user_sa.id,
            full_name=user_sa.full_name,
            email=user_sa.email,
        )

    def _task_to_task_response(self, task_sa: Task | None) -> TaskResponse | None:
        if not task_sa:
            return None
        return TaskResponse(
            id=task_sa.id,
            title=task_sa.title,
            description=task_sa.description,
            status=task_sa.status,
            created_at=task_sa.created_at,
            column_id=task_sa.column_id,
            board_id=task_sa.board_id,
            sprint_id=task_sa.sprint_id,
            group_id=task_sa.group_id,
            author=self._user_to_userdb(task_sa.author),
            author_id=task_sa.author_id,
            observers=[self._user_to_userdb(obs) for obs in task_sa.observers] if task_sa.observers else [],
        )

    async def created_task(self, task_data: TaskCreateRequest) -> TaskResponse:
        async with self.uow:
            new_task_sa = Task(
                title=task_data.title,
                description=task_data.description,
                status=task_data.status,
                author_id=task_data.author_id,
                column_id=task_data.column_id,
                board_id=task_data.board_id,
                sprint_id=task_data.sprint_id,
                group_id=task_data.group_id,
            )
            if task_data.observer_ids:
                observers = await self._get_users_by_ids(task_data.observer_ids)
                new_task_sa.observers.extend(observers)

            created_task_sa = await self.uow.task.create(new_task_sa)

            task_with_relations = await self.uow.task.get_with_relations(created_task_sa.id)
            if not task_with_relations:
                raise HTTPException(status_code=500, detail="Failed to retrieve created task with relations")

            return self._task_to_task_response(task_with_relations)

    async def get_task(self, task_id: UUID4) -> TaskResponse | None:
        async with self.uow:
            task_sa = await self.uow.task.get_with_relations(task_id)
            return self._task_to_task_response(task_sa)

    async def get_all_tasks(self, author_id: UUID4 | None = None, status: str | None = None) -> TaskListResponse:
        async with self.uow:
            tasks_sa = await self.uow.task.get_all_with_relations()

            filtered_tasks = []
            for task in tasks_sa:
                if author_id is not None and task.author_id != author_id:
                    continue
                if status is not None and task.status.value != status:
                    continue
                filtered_tasks.append(task)

            return TaskListResponse(tasks=[self._task_to_task_response(task) for task in filtered_tasks])

    async def update_task(self, task_id: UUID4, task_data: TaskUpdateRequest) -> TaskResponse | None:
        async with self.uow:
            existing_task_sa = await self.uow.task.get_with_relations(task_id)
            if not existing_task_sa:
                return None

            update_data = task_data.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                if key != 'observer_ids':
                    setattr(existing_task_sa, key, value)

            if 'author_id' in update_data and update_data['author_id'] is not None:
                new_author = await self.uow.user._get_users_by_ids(update_data['author_id'])
                if not new_author:
                    raise HTTPException(status_code=400, detail=f"Author with ID {update_data['author_id']} not found.")
                existing_task_sa.author = new_author
            elif 'author_id' in update_data and update_data['author_id'] is None:  # Если явно передали null
                existing_task_sa.author = None

            if 'executor_id' in update_data and update_data['executor_id'] is not None:
                new_executor = await self.uow.user.get_by_id(update_data['executor_id'])
                if not new_executor:
                    raise HTTPException(status_code=400,
                                        detail=f"Executor with ID {update_data['executor_id']} not found.")
                existing_task_sa.executor = new_executor
            elif 'executor_id' in update_data and update_data['executor_id'] is None:  # Если явно передали null
                existing_task_sa.executor = None

            if 'observer_ids' in update_data and update_data['observer_ids'] is not None:
                existing_task_sa.observers.clear()
                if update_data['observer_ids']:
                    new_observers = await self._get_users_by_ids(update_data['observer_ids'])
                    existing_task_sa.observers.extend(new_observers)

            await self.uow._session.flush()
            task_with_relations = await self.uow.task.get_with_relations(existing_task_sa.id)
            # updated_task_sa = await self.uow.task.update(existing_task_sa)
            return self._task_to_task_response(task_with_relations)

    async def delete_task(self, task_id: UUID4) -> None:
        async with self.uow:
            await self.uow.task.delete(task_id)

    async def _get_users_by_ids(self, user_ids: List[UUID4]) -> Sequence[User]:

        async with self.uow:
            result = await self.uow._session.execute(select(User).where(User.id.in_(user_ids)))
            users = result.scalars().all()
            if len(users) != len(user_ids):
                found_ids = {u.id for u in users}
                missing_ids = [str(uid) for uid in user_ids if uid not in found_ids]
                raise HTTPException(status_code=400, detail=f"Users not found: {', '.join(missing_ids)}")
            return users