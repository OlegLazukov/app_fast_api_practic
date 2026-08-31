__all__ = [
    'router'
]


from fastapi import APIRouter
from src.api.v1.routers import task, user, board, column, sprint, group


router = APIRouter()


router.include_router(user.router_user, prefix='/users', tags=['User | v1'])
router.include_router(task.router_task, prefix='/tasks', tags=['Task | v1'])
router.include_router(board.router_board, prefix='/boards', tags=['Board | v1'])
router.include_router(column.router_column, prefix='/columns', tags=['Column | v1'])
router.include_router(sprint.router_sprint, prefix='/sprints', tags=['Sprint | v1'])
router.include_router(group.router_group, prefix='/groups', tags=['Group | v1'])



