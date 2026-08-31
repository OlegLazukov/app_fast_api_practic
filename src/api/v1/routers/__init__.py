__all__ = [
    'v1_router_user',
    'v1_router_task',
    'v1_router_group',
    'v1_router_board',
    'v1_router_sprint',
    'v1_router_column',
]

from src.api.v1.routers.user import router_user as v1_router_user
from src.api.v1.routers.task import router_task as v1_router_task
from src.api.v1.routers.group import router_group as v1_router_group
from src.api.v1.routers.board import router_board as v1_router_board
from src.api.v1.routers.sprint import router_sprint as v1_router_sprint
from src.api.v1.routers.column import router_column as v1_router_column