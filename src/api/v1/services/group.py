from typing import Sequence, Optional
from uuid import UUID
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from src.schemas.input import GroupCreateRequest, GroupUpdateRequest
from src.models.models import Group
from src.utils.unit_of_work import UnitOfWork


class GroupService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    async def create_group(self, group_data: GroupCreateRequest) -> Group:
        async with self.uow:
            existing_group = await self.uow._session.execute(
                select(Group).where(Group.name == Group.name)
            )
            if existing_group.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Group with this name already exists")
            new_group = await self.uow.group.create(Group(**group_data.model_dump()))
            return new_group

    async def get_all_groups(self) -> Sequence[Group]:
        async with self.uow:
            return await self.uow.group.get_all()

    async def get_group(self, group_id: UUID) -> Optional[Group]:
        async with self.uow:
            return await self.uow.group.get_by_id(group_id)

    async def update_group(self, group_id: UUID, group_data: GroupUpdateRequest) -> Optional[Group]:
        async with self.uow:
            existing_group = await self.uow.group.get_by_id(group_id)
            if not existing_group:
                return None

            update_dict = group_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(existing_group, key, value)

            updated_group = await self.uow.group.update(existing_group, update_dict)
            return updated_group

    async def delete_group(self, group_id: UUID) -> None:
        async with self.uow:
            group_sa = await self.uow.group.get_by_id(group_id)
            if not group_sa:
                raise HTTPException(status_code=404, detail="Group not found")
            await self.uow.group.delete(group_id)