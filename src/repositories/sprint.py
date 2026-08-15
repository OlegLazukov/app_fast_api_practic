from typing import Optional
from uuid import UUID
from sqlalchemy import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import Sprint

class SprintRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, sprint: Sprint) -> Sprint:
        self.session.add(sprint)
        await self.session.commit()
        await self.session.refresh(sprint)
        return sprint

    async def get_by_id(self, sprint_id: UUID) -> Optional[Sprint]:
        result = await self.session.execute(
            select(Sprint).where(Sprint.id == sprint_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Sprint]:
        result = await self.session.execute(select(Sprint))
        return result.scalars().all()

    async def update(self, sprint: Sprint, update_data: dict) -> Sprint:
        for key, value in update_data.items():
            setattr(sprint, key, value)
        await self.session.commit()
        await self.session.refresh(sprint)
        return sprint

    async def delete(self, sprint_id: UUID) -> None:
        sprint = await self.get_by_id(sprint_id)
        await self.session.delete(sprint)
        await self.session.commit()