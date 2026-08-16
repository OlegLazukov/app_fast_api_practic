from typing import Optional
from src.utils.repository import SqlAlchemyRepository
from sqlalchemy import select
from src.models.models import Board

class BoardRepository(SqlAlchemyRepository[Board]):
    _model = Board
    async def get_by_name(self, name: str) -> Optional[Board]:
        query = select(self._model).where(self._model.name == name)
        res = await self._session.execute(query)
        return res.scalar_one_or_none()
