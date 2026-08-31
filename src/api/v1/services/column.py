from typing import Optional, Sequence
from uuid import UUID
from src.schemas.column import ColumnCreateRequest, ColumnUpdateRequest
from src.models.models import Column
from src.utils.service import BaseService, transaction_mode
from src.utils.constants import COLUMN_EXIST_MSG, COLUMN_NOT_FOUND_MSG
from src.repositories.column import ColumnRepository



class ColumnService(BaseService, ColumnRepository):

    _repo: str = "column"

    @transaction_mode
    async def create_column(self, column_data: ColumnCreateRequest) -> Column:
        existing_column = await self.uow.column.get_by_name(name=column_data.name)
        if existing_column:
            self.check_existence(obj=column_data, details=COLUMN_EXIST_MSG)

        new_column = await self.add_one_and_get_obj(**column_data.model_dump())
        return new_column

    @transaction_mode
    async def get_all_columns(self) -> Sequence[Column]:
        return await self.get_by_filter_all()

    @transaction_mode
    async def get_column_by_id(self, column_id: UUID) -> Optional[Column]:
        column = await self.get_by_filter_one_or_none(id=column_id)
        self.check_existence(column, details=COLUMN_NOT_FOUND_MSG)
        return column

    @transaction_mode
    async def update_column_by_id(self, column_id: UUID, column_data: ColumnUpdateRequest) -> Optional[Column]:
        existing_column = await self.get_by_filter_one_or_none(id=column_id)
        if not existing_column:
            self.check_existence(existing_column, details=COLUMN_NOT_FOUND_MSG)

        updated_column = await self.update_one_by_id(obj_id=column_id, **column_data.model_dump(exclude_unset=True))
        return updated_column

    @transaction_mode
    async def delete_column_by_id(self, column_id: UUID) -> None:
        existing_column = await self.get_by_filter_one_or_none(id=column_id)
        self.check_existence(existing_column, details=COLUMN_NOT_FOUND_MSG)

        await self.delete_by_ids(column_id)