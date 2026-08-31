from typing import Optional, Sequence
from uuid import UUID
from src.schemas.sprint import SprintCreateRequest, SprintUpdateRequest
from src.models.models import Sprint
from src.utils.service import BaseService, transaction_mode
from src.utils.constants import SPRINT_NOT_FOUND_MSG, SPRINT_EXIST_MSG
from src.repositories.sprint import SprintRepository



class SprintService(BaseService, SprintRepository):

    _repo: str = "sprint"

    @transaction_mode
    async def create_sprint(self, sprint_data: SprintCreateRequest) -> Sprint:
        existing_sprint = await self.uow.sprint.get_by_name(name=sprint_data.name)
        if existing_sprint:
            self.check_existence(obj=sprint_data, details=SPRINT_EXIST_MSG)

        new_sprint = await self.add_one_and_get_obj(**sprint_data.model_dump())
        return new_sprint

    @transaction_mode
    async def get_all_sprints(self) -> Sequence[Sprint]:
        return await self.get_by_filter_all()

    @transaction_mode
    async def get_sprint_by_id(self, board_id: UUID) -> Optional[Sprint]:
        board = await self.get_by_filter_one_or_none(id=board_id)
        self.check_existence(board, details=SPRINT_NOT_FOUND_MSG)
        return board

    @transaction_mode
    async def update_sprint_by_id(self, sprint_id: UUID, sprint_data: SprintUpdateRequest) -> Optional[Sprint]:
        existing_sprint = await self.get_by_filter_one_or_none(id=sprint_id)
        if not existing_sprint:
            self.check_existence(existing_sprint, details=SPRINT_NOT_FOUND_MSG)

        updated_sprint = await self.update_one_by_id(obj_id=sprint_id, **sprint_data.model_dump(exclude_unset=True))
        return updated_sprint

    @transaction_mode
    async def delete_sprint_by_id(self, sprint_id: UUID) -> None:
        existing_sprint = await self.get_by_filter_one_or_none(id=sprint_id)
        self.check_existence(existing_sprint, details=SPRINT_NOT_FOUND_MSG)

        await self.delete_by_ids(sprint_id)