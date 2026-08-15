from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from src.schemas.input import BoardCreateRequest, BoardUpdateRequest
from src.models.models import Board
from src.utils.unit_of_work import UnitOfWork

class BoardService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    async def create_board(self, board_data: BoardCreateRequest) -> Board:
        async with self.uow:
            existing_board = await self.uow._session.execute(
                select(Board).where(Board.name == board_data.name)
            )
            if existing_board.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Board with this name already exists")

            board = Board(
                name=board_data.name,
            )
            new_board = await self.uow.board.create(board)
            return new_board

    async def get_all_boards(self) -> Sequence[Board]:
        async with self.uow:
            return await self.uow.board.get_all()

    async def get_board(self, board_id: UUID) -> Optional[Board]:
        async with self.uow:
            board_sa = await self.uow.board.get_by_id(board_id)
            if not board_sa:
                raise HTTPException(status_code=404, detail="User not found")
            return board_sa


    async def update_board(self, board_id: UUID, board_data: BoardUpdateRequest) -> Optional[Board]:
        async with self.uow:
            existing_board = await self.uow.board.get_by_id(board_id)
            if not existing_board:
                return None

            update_dict = board_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(existing_board, key, value)

            updated_board = await self.uow.board.update(existing_board, update_dict)
            return updated_board

    async def delete_board(self, board_id: UUID) -> None:
        async with self.uow:
            board_sa = await self.uow.board.get_by_id(board_id)
            if not board_sa:
                raise HTTPException(status_code=404, detail="Board not found")
            await self.uow.board.delete(board_id)