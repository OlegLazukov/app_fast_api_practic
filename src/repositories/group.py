from typing import Optional
from sqlalchemy import select
from src.models.models import Group
from src.utils.repository import SqlAlchemyRepository


class GroupRepository(SqlAlchemyRepository[Group]):
    _model = Group

    async def get_by_name(self, name: str) -> Optional[Group]:
        query = select(self._model).where(self._model.name == name)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()