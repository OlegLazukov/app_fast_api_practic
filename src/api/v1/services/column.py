from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from src.schemas.input import ColumnCreateRequest, ColumnUpdateRequest
from src.models.models import Column
from src.utils.unit_of_work import UnitOfWork


class ColumnService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    async def create_column(self, column_data: ColumnCreateRequest) -> Column:
        async with self.uow:
            existing_group = await self.uow._session.execute(
                select(Column).where(Column.name == Column.name)
            )
            if existing_group.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Column with this name already exists")
            board = await self.uow.board.get_by_id(column_data.board_id)
            if not board:
                raise ValueError(f"Column with ID {column_data.board_id} does not exist.")

            new_column = await self.uow.column.create(Column(**column_data.model_dump()))
            return new_column

    async def get_all_columns(self) -> Sequence[Column]:
        async with self.uow:
            return await self.uow.column.get_all()

    async def get_column(self, column_id: UUID) -> Optional[Column]:
        async with self.uow:
            column_sa = await self.uow.column.get_by_id(column_id)
            if not column_sa:
                raise HTTPException(status_code=404, detail="Column not found")
            return column_sa


    async def update_column(self, column_id: UUID, column_data: ColumnUpdateRequest) -> Optional[Column]:
        async with self.uow:
            existing_column = await self.uow.column.get_by_id(column_id)
            if not existing_column:
                return None

            update_dict = column_data.model_dump(exclude_unset=True)

            if "column_id" in update_dict and update_dict["column_id"] is not None:
                board = await self.uow.board.get_by_id(update_dict["column_id"])
                if not board:
                    raise ValueError(f"Column with ID {update_dict['column_id']} does not exist.")

            for key, value in update_dict.items():
                setattr(existing_column, key, value)

            updated_column = await self.uow.column.update(existing_column, update_dict)
            return updated_column

    async def delete_column(self, column_id: UUID) -> None:
        async with self.uow:
            column_sa = await self.uow.column.get_by_id(column_id)
            if not column_sa:
                raise HTTPException(status_code=404, detail="Column not found")
            await self.uow.column.delete(column_id)