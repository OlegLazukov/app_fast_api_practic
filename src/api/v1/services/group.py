from typing import Optional, Sequence
from uuid import UUID
from src.schemas.group import GroupCreateRequest, GroupUpdateRequest
from src.models.models import Group
from src.utils.service import BaseService, transaction_mode
from src.utils.constants import GROUP_EXIST_MSG, GROUP_NOT_FOUND_MSG
from src.repositories.group import GroupRepository



class GroupService(BaseService, GroupRepository):

    _repo: str = "group"

    @transaction_mode
    async def create_group(self, group_data: GroupCreateRequest) -> Group:
        existing_group = await self.uow.group.get_by_name(name=group_data.name)
        if existing_group:
            self.check_existence(obj=group_data, details=GROUP_EXIST_MSG)

        new_group = await self.add_one_and_get_obj(**group_data.model_dump())
        return new_group

    @transaction_mode
    async def get_all_groups(self) -> Sequence[Group]:
        return await self.get_by_filter_all()

    @transaction_mode
    async def get_group_by_id(self, group_id: UUID) -> Optional[Group]:
        group = await self.get_by_filter_one_or_none(id=group_id)
        self.check_existence(group, details=GROUP_NOT_FOUND_MSG)
        return group

    @transaction_mode
    async def update_group_by_id(self, group_id: UUID, group_data: GroupUpdateRequest) -> Optional[Group]:
        existing_group = await self.get_by_filter_one_or_none(id=group_id)
        if not existing_group:
            self.check_existence(existing_group, details=GROUP_NOT_FOUND_MSG)

        updated_group = await self.update_one_by_id(obj_id=group_id, **group_data.model_dump(exclude_unset=True))
        return updated_group

    @transaction_mode
    async def delete_group_by_id(self, group_id: UUID) -> None:
        existing_group = await self.get_by_filter_one_or_none(id=group_id)
        self.check_existence(existing_group, details=GROUP_NOT_FOUND_MSG)

        await self.delete_by_ids(group_id)