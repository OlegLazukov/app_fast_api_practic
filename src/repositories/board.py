from typing import Optional
from uuid import UUID
from sqlalchemy import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models.models import Board

class BoardRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, board: Board) -> Board:
        self.session.add(board)
        await self.session.commit()
        await self.session.refresh(board)
        return board

    async def get_by_id(self, board_id: UUID) -> Optional[Board]:
        result = await self.session.execute(
            select(Board).where(Board.id == board_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> Sequence[Board]:
        result = await self.session.execute(select(Board))
        return result.scalars().all()

    async def update(self, board: Board, update_data: dict) -> Board:
        for key, value in update_data.items():
            setattr(board, key, value)
        await self.session.commit()
        await self.session.refresh(board)
        return board

    async def delete(self, board_id: UUID) -> None:
        board = await self.get_by_id(board_id)
        await self.session.delete(board)
        await self.session.commit()