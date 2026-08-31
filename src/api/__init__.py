__all__ = [
    'router'
]

import asyncio

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from loguru import logger
from src.api.v1.routers import task, user, board, column, sprint, group
from src.database import get_async_session
from src.schemas.response import BaseResponse


router = APIRouter()


router.include_router(user.router_user, prefix='/users', tags=['User | v1'])
router.include_router(task.router_task, prefix='/tasks', tags=['Task | v1'])
router.include_router(board.router_board, prefix='/boards', tags=['Board | v1'])
router.include_router(column.router_column, prefix='/columns', tags=['Column | v1'])
router.include_router(sprint.router_sprint, prefix='/sprints', tags=['Sprint | v1'])
router.include_router(group.router_group, prefix='/groups', tags=['Group | v1'])



@router.get(
    path='/healthz/',
    tags=['healthz'],
    status_code=HTTP_200_OK,
)
async def health_check(
        session: AsyncSession = Depends(get_async_session),
) -> BaseResponse:
    """Check api external connection."""
    async def check_service(service: str) -> None:
        try:
            if service == 'postgres':
                await session.execute(text('SELECT 1'))
        except Exception as exc:
            logger.error(f'Health check failed with error: {exc}')
            raise HTTPException(status_code=HTTP_400_BAD_REQUEST)

    await asyncio.gather(*[
        check_service('postgres'),
    ])

    return BaseResponse()