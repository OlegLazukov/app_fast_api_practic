from typing import Optional, Sequence
from uuid import UUID
from sqlalchemy.future import select
from fastapi import Depends, HTTPException
from src.schemas.input import SprintCreateRequest, SprintUpdateRequest
from src.models.models import Sprint
from src.utils.unit_of_work import UnitOfWork


class SprintService:
    def __init__(self, uow: UnitOfWork = Depends(UnitOfWork.get_uow)):
        self.uow = uow

    async def create_sprint(self, sprint_data: SprintCreateRequest) -> Sprint:
        async with self.uow:
            existing_sprint = await self.uow._session.execute(
                select(Sprint).where(Sprint.name == Sprint.name)
            )
            if existing_sprint.scalar_one_or_none():
                raise HTTPException(status_code=409, detail="Sprint with this name already exists")
            new_sprint = await self.uow.sprint.create(Sprint(**sprint_data.model_dump()))
            return new_sprint

    async def get_all_sprints(self) -> Sequence[Sprint]:
        async with self.uow:
            return await self.uow.sprint.get_all()

    async def get_sprint(self, sprint_id: UUID) -> Optional[Sprint]:
        async with self.uow:
            return await self.uow.sprint.get_by_id(sprint_id)

    async def update_sprint(self, sprint_id: UUID, sprint_data: SprintUpdateRequest) -> Optional[Sprint]:
        async with self.uow:
            existing_sprint = await self.uow.sprint.get_by_id(sprint_id)
            if not existing_sprint:
                return None

            update_dict = sprint_data.model_dump(exclude_unset=True)
            for key, value in update_dict.items():
                setattr(existing_sprint, key, value)

            updated_sprint = await self.uow.sprint.update(existing_sprint, update_dict)
            return updated_sprint

    async def delete_sprint(self, sprint_id: UUID) -> None:
        async with self.uow:
            sprint_sa = await self.uow.sprint.get_by_id(sprint_id)
            if not sprint_sa:
                raise HTTPException(status_code=404, detail="Sprint not found")
            await self.uow.sprint.delete(sprint_id)