from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import UUID4
from typing import List

from src.api.v1.services.group import GroupService
from src.schemas.group import GroupCreateRequest, GroupUpdateRequest, GroupResponse

from src.utils.constants import GROUP_NOT_FOUND_MSG

router_group = APIRouter(prefix="/groups")

@router_group.post(
    "/",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Создать новую группу"
)
async def create_group(
    group_data: GroupCreateRequest,
    service: GroupService = Depends(GroupService)
) -> GroupResponse:
    """Создает новую группу."""
    new_group = await service.create_group(group_data)
    return GroupResponse.model_validate(new_group)

@router_group.get(
    "/",
    response_model=List[GroupResponse],
    status_code=status.HTTP_200_OK,
    summary="Получить список всех групп"
)
async def get_all_groups(
    service: GroupService = Depends(GroupService)
) -> List[GroupResponse]:
    """Возвращает список всех существующих групп."""
    groups = await service.get_all_groups()
    return [GroupResponse.model_validate(group) for group in groups]

@router_group.get(
    "/{group_id}",
    response_model=GroupResponse,
    status_code=status.HTTP_200_OK,
    summary="Получить группу по ID"
)
async def get_group(
    group_id: UUID4,
    service: GroupService = Depends(GroupService)
) -> GroupResponse:
    """Возвращает информацию о группе по её уникальному идентификатору."""
    group = await service.get_group_by_id(group_id)
    if not group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=GROUP_NOT_FOUND_MSG)
    return GroupResponse.model_validate(group)

@router_group.put(
    "/{group_id}",
    response_model=GroupResponse,
    status_code=status.HTTP_200_OK,
    summary="Обновить группу по ID"
)
async def update_group(
    group_id: UUID4,
    group_data: GroupUpdateRequest,
    service: GroupService = Depends(GroupService)
) -> GroupResponse:
    """Обновляет информацию о группе по её уникальному идентификатору."""
    updated_group = await service.update_group_by_id(group_id, group_data)
    if not updated_group:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=GROUP_NOT_FOUND_MSG)
    return GroupResponse.model_validate(updated_group)

@router_group.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить группу по ID"
)
async def delete_group(
    group_id: UUID4,
    service: GroupService = Depends(GroupService)
) -> None:
    """Удаляет группу по её уникальному идентификатору."""
    await service.delete_group_by_id(group_id)