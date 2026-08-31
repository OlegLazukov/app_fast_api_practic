from typing import Optional, List
from sqlalchemy import Sequence
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import UUID
from src.models.models import Task
from src.utils.repository import SqlAlchemyRepository


class TaskRepository(SqlAlchemyRepository[Task]):
    _model = Task

    async def get_by_name(self, title: str) -> Optional[Task]:
        query = select(self._model).where(self._model.title == title)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()

    async def get_with_relations(self, task_id: UUID) -> Task | None:
        result = await self._session.execute(
            select(Task)
            .options(
                selectinload(Task.author),
                selectinload(Task.observers)
            )
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_all_with_relations(self) -> Sequence[Task]:
        result = await self._session.execute(
            select(Task)
            .options(
                selectinload(Task.author),
                selectinload(Task.observers)
            )
        )
        return result.scalars().all()

