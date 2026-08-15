from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import List

from src.api.v1.services.column import ColumnService
from src.schemas.input import ColumnCreateRequest, ColumnUpdateRequest
from src.schemas.output import ColumnResponse

router_column = APIRouter(prefix="/columns")

@router_column.post(
    "/",
    response_model=ColumnResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую колонку"
)
async def create_column(
    column_data: ColumnCreateRequest,
    service: ColumnService = Depends(ColumnService)
) -> ColumnResponse:
    """Создает новую колонку, привязанную к существующей доске."""
    try:
        new_column = await service.create_column(column_data)
        return ColumnResponse.model_validate(new_column)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

@router_column.get(
    "/",
    response_model=List[ColumnResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех колонок"
)
async def get_all_columns(
    service: ColumnService = Depends(ColumnService)
) -> List[ColumnResponse]:
    """Возвращает список всех существующих колонок."""
    columns = await service.get_all_columns()
    return [ColumnResponse.model_validate(column) for column in columns]

@router_column.get(
    "/{column_id}",
    response_model=ColumnResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить колонку по ID"
)
async def get_column(
    column_id: UUID4,
    service: ColumnService = Depends(ColumnService) # Зависимость на сервис
) -> ColumnResponse:
    """Возвращает информацию о колонке по её уникальному идентификатору."""
    column = await service.get_column(column_id)
    if not column:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
    return ColumnResponse.model_validate(column)

@router_column.put(
    "/{column_id}",
    response_model=ColumnResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить колонку по ID"
)
async def update_column(
    column_id: UUID4,
    column_data: ColumnUpdateRequest,
    service: ColumnService = Depends(ColumnService)
) -> ColumnResponse:
    """Обновляет информацию о колонке по её уникальному идентификатору."""
    try:
        updated_column = await service.update_column(column_id, column_data)
        if not updated_column:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Column not found")
        return ColumnResponse.model_validate(updated_column)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router_column.delete(
    "/{column_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить колонку по ID"
)
async def delete_column(
    column_id: UUID4,
    service: ColumnService = Depends(ColumnService)
) -> None:
    """Удаляет колонку по её уникальному идентификатору."""
    await service.delete_column(column_id)