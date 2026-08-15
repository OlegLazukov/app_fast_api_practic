from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import List

from src.api.v1.services.board import BoardService
from src.schemas.input import BoardCreateRequest, BoardUpdateRequest
from src.schemas.output import BoardResponse

router_board = APIRouter(prefix="/boards")

@router_board.post(
    "/",
    response_model=BoardResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую доску"
)
async def create_board(
    board_data: BoardCreateRequest,
    service: BoardService = Depends(BoardService)
) -> BoardResponse:
    """Создает новую доску."""
    new_board = await service.create_board(board_data)
    return BoardResponse.model_validate(new_board)

@router_board.get(
    "/",
    response_model=List[BoardResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех досок"
)
async def get_all_boards(
    service: BoardService = Depends(BoardService)
) -> List[BoardResponse]:
    """Возвращает список всех существующих досок."""
    boards = await service.get_all_boards()
    return [BoardResponse.model_validate(board) for board in boards]

@router_board.get(
    "/{board_id}",
    response_model=BoardResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить доску по ID"
)
async def get_board(
    board_id: UUID4,
    service: BoardService = Depends(BoardService)
) -> BoardResponse:
    """Возвращает информацию о доске по её уникальному идентификатору."""
    board = await service.get_board(board_id)
    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return BoardResponse.model_validate(board)

@router_board.put(
    "/{board_id}",
    response_model=BoardResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить доску по ID"
)
async def update_board(
    board_id: UUID4,
    board_data: BoardUpdateRequest,
    service: BoardService = Depends(BoardService)
) -> BoardResponse:
    """Обновляет информацию о доске по её уникальному идентификатору."""
    updated_board = await service.update_board(board_id, board_data)
    if not updated_board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Board not found")
    return BoardResponse.model_validate(updated_board)

@router_board.delete(
    "/{board_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить доску по ID"
)
async def delete_board(
    board_id: UUID4,
    service: BoardService = Depends(BoardService)
) -> None:
    """Удаляет доску по её уникальному идентификатору."""
    await service.delete_board(board_id)
