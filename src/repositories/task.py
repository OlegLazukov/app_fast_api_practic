from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy.dialects.postgresql import UUID

from src.models.models import Task

class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, task: Task) -> Task:
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: UUID) -> Task | None:
        result = await self.session.execute(select(Task).where(Task.id == task_id))
        return result.scalar_one_or_none()

    async def get_with_relations(self, task_id: UUID) -> Task | None:
        result = await self.session.execute(
            select(Task)
            .options(
                selectinload(Task.author),
                selectinload(Task.observers)
            )
            .where(Task.id == task_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self, query) -> Sequence[Task]:
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_with_relations(self) -> Sequence[Task]:
        result = await self.session.execute(
            select(Task)
            .options(
                selectinload(Task.author),
                selectinload(Task.observers)
            )
        )
        return result.scalars().all()

    async def update(self, task: Task) -> Task:
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete(self, task_id: UUID) -> Task | None:
        task = await self.get(task_id)
        if task:
            await self.session.delete(task)
            await self.session.commit()
        return task