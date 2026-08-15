from sqlalchemy import Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.dialects.postgresql import UUID

from src.models.models import User

class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: User) -> User:
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def get(self, user_id: UUID) -> User | None:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[User]:
        result = await self.session.execute(select(User))
        return result.scalars().all()

    async def update(self, user: User) -> User:
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, user_id: UUID) -> User | None:
        user = await self.get(user_id)
        if user:
            await self.session.delete(user)
            await self.session.commit()
        return user

    async def get_by_filters(self, query) -> Sequence[User]:
        result = await self.session.execute(query)
        return result.scalars().all()