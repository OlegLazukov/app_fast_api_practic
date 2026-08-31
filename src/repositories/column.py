from typing import Optional
from sqlalchemy import select
from src.models.models import Column
from src.utils.repository import SqlAlchemyRepository


class ColumnRepository(SqlAlchemyRepository[Column]):
    _model = Column

    async def get_by_name(self, name: str) -> Optional[Column]:
        query = select(self._model).where(self._model.name == name)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()