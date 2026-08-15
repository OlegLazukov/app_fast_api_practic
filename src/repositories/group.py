from typing import Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import Group
from sqlalchemy import Sequence


class GroupRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, group: Group) -> Group:
        self.session.add(group)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def get_by_id(self, group_id: UUID) -> Optional[Group]:
        result = await self.session.execute(
            select(Group).where(Group.id == group_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Group]:
        result = await self.session.execute(select(Group))
        return result.scalars().all()

    async def update(self, group: Group, update_data: dict) -> Group:
        for key, value in update_data.items():
            setattr(group, key, value)
        await self.session.commit()
        await self.session.refresh(group)
        return group

    async def delete(self, group_id: UUID) -> None:
        group = await self.get_by_id(group_id)
        await self.session.delete(group)
        await self.session.commit()