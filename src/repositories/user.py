from typing import Optional
from sqlalchemy import Sequence
from sqlalchemy.future import select
from src.models.models import User
from src.utils.repository import SqlAlchemyRepository


class UserRepository(SqlAlchemyRepository[User]):
    _model = User

    async def get_by_email(self, email: str) -> Optional[User]:
        query = select(self._model).filter_by(email=email)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()


    async def get_by_filters(self, full_name: str | None = None, email: str | None = None) -> Sequence[User]:
        query = select(self._model)
        if full_name:
            query = query.filter(self._model.full_name.ilike(f"%{full_name}%"))
        if email:
            query = query.filter(self._model.email.ilike(f"%{email}%"))

        res = await self._session.execute(query)
        return res.scalars().all()