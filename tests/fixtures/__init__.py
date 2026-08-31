
__all__ = [
    'TaskService',
    'FakeBaseService',
    'FakeUnitOfWork',
    'UserService',
    'BoardService',
    'ColumnService',
    'GroupService',
    'SprintService',
    'db_mocks',
    'testing_cases',
]

from types import TracebackType

from sqlalchemy.ext.asyncio import AsyncSession

from src.api.v1.services import (
    TaskService,
    UserService,
    BoardService,
    GroupService,
    ColumnService,
    SprintService
)
from src.repositories import (
    TaskRepository,
    UserRepository,
    GroupRepository,
    SprintRepository,
    BoardRepository,
    ColumnRepository
)
from src.utils.service import BaseService
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import db_mocks, testing_cases


class FakeUnitOfWork(UnitOfWork):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self._session = session

    async def __aenter__(self) -> None:
        self.task = TaskRepository(self._session)
        self.user = UserRepository(self._session)
        self.group = GroupRepository(self._session)
        self.sprint = SprintRepository(self._session)
        self.board = BoardRepository(self._session)
        self.column = ColumnRepository(self._session)

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self._session.flush()


class FakeBaseService(BaseService):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__()
        self.uow = FakeUnitOfWork(session)