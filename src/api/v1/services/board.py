from typing import Optional, Sequence
from uuid import UUID
from src.schemas.board import BoardCreateRequest, BoardUpdateRequest
from src.models.models import Board
from src.utils.service import BaseService, transaction_mode
from src.utils.constants import BOARD_NOT_FOUND_MSG, BOARD_EXIST_MSG
from src.repositories.board import BoardRepository



class BoardService(BaseService, BoardRepository):

    _repo: str = "board"

    @transaction_mode
    async def create_board(self, board_data: BoardCreateRequest) -> Board:
        existing_board = await self.uow.board.get_by_name(name=board_data.name)
        if existing_board:
            self.check_existence(obj=board_data, details=BOARD_EXIST_MSG)

        new_board = await self.add_one_and_get_obj(**board_data.model_dump())
        return new_board

    @transaction_mode
    async def get_all_boards(self) -> Sequence[Board]:
        return await self.get_by_filter_all()

    @transaction_mode
    async def get_board_by_id(self, board_id: UUID) -> Optional[Board]:
        board = await self.get_by_filter_one_or_none(id=board_id)
        self.check_existence(board, details=BOARD_NOT_FOUND_MSG)
        return board

    @transaction_mode
    async def update_board_by_id(self, board_id: UUID, board_data: BoardUpdateRequest) -> Optional[Board]:
        existing_board = await self.get_by_filter_one_or_none(id=board_id)
        if not existing_board:
            self.check_existence(existing_board, details=BOARD_NOT_FOUND_MSG)

        updated_board = await self.update_one_by_id(obj_id=board_id, **board_data.model_dump(exclude_unset=True))
        return updated_board

    @transaction_mode
    async def delete_board_by_id(self, board_id: UUID) -> None:
        existing_board = await self.get_by_filter_one_or_none(id=board_id)
        self.check_existence(existing_board, details=BOARD_NOT_FOUND_MSG)

        await self.delete_by_ids(board_id)