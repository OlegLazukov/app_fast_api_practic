from typing import Optional
from uuid import UUID
from sqlalchemy import Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import Column

class ColumnRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, column: Column) -> Column:
        self.session.add(column)
        await self.session.commit()
        await self.session.refresh(column)
        return column

    async def get_by_id(self, column_id: UUID) -> Optional[Column]:
        result = await self.session.execute(
            select(Column).where(Column.id == column_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Column]:
        result = await self.session.execute(select(Column))
        return result.scalars().all()

    async def update(self, column: Column, update_data: dict) -> Column:
        for key, value in update_data.items():
            setattr(column, key, value)
        await self.session.commit()
        await self.session.refresh(column)
        return column

    async def delete(self, column_id: UUID) -> None:
        column = await self.get_by_id(column_id)
        await self.session.delete(column)
        await self.session.commit()