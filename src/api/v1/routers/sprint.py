from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import List

from src.api.v1.services.sprint import SprintService
from src.schemas.input import SprintCreateRequest, SprintUpdateRequest
from src.schemas.output import SprintResponse

router_sprint = APIRouter(prefix="/sprints")

@router_sprint.post(
    "/",
    response_model=SprintResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новый спринт"
)
async def create_sprint(
    sprint_data: SprintCreateRequest,
    service: SprintService = Depends(SprintService)
) -> SprintResponse:
    """Создает новый спринт."""
    new_sprint = await service.create_sprint(sprint_data)
    return SprintResponse.model_validate(new_sprint)

@router_sprint.get(
    "/",
    response_model=List[SprintResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех спринтов"
)
async def get_all_sprints(
    service: SprintService = Depends(SprintService)
) -> List[SprintResponse]:
    """Возвращает список всех существующих спринтов."""
    sprints = await service.get_all_sprints()
    return [SprintResponse.model_validate(sprint) for sprint in sprints]

@router_sprint.get(
    "/{sprint_id}",
    response_model=SprintResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить спринт по ID"
)
async def get_sprint(
    sprint_id: UUID4,
    service: SprintService = Depends(SprintService)
) -> SprintResponse:
    """Возвращает информацию о спринте по его уникальному идентификатору."""
    sprint = await service.get_sprint(sprint_id)
    if not sprint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sprint not found")
    return SprintResponse.model_validate(sprint)

@router_sprint.put(
    "/{sprint_id}",
    response_model=SprintResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить спринт по ID"
)
async def update_sprint(
    sprint_id: UUID4,
    sprint_data: SprintUpdateRequest,
    service: SprintService = Depends(SprintService)
) -> SprintResponse:
    """Обновляет информацию о спринте по его уникальному идентификатору."""
    updated_sprint = await service.update_sprint(sprint_id, sprint_data)
    if not updated_sprint:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Sprint not found")
    return SprintResponse.model_validate(updated_sprint)

@router_sprint.delete(
    "/{sprint_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить спринт по ID"
)
async def delete_sprint(
    sprint_id: UUID4,
    service: SprintService = Depends(SprintService)
) -> None:
    """Удаляет спринт по его уникальному идентификатору."""
    await service.delete_sprint(sprint_id)