from typing import Optional
from sqlalchemy import select
from src.models.models import Sprint
from src.utils.repository import SqlAlchemyRepository


class SprintRepository(SqlAlchemyRepository[Sprint]):
    _model = Sprint

    async def get_by_name(self, name: str) -> Optional[Sprint]:
        query = select(self._model).where(self._model.name == name)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()