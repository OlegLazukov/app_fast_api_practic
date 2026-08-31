from collections.abc import Sequence
from copy import deepcopy
from typing import Callable, Awaitable, Any

import pytest
import pytest_asyncio
from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import User, Group, Sprint, Board, Column, Task
from tests import fixtures
from tests.utils import bulk_save_models

@pytest_asyncio.fixture
async def setup_users(transaction_session: AsyncSession, users: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, User, users)

@pytest_asyncio.fixture
async def setup_groups(setup_users: None, transaction_session: AsyncSession, groups: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Group, groups)

@pytest_asyncio.fixture
async def setup_sprints(setup_groups: None, transaction_session: AsyncSession, sprints: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Sprint, sprints)

@pytest_asyncio.fixture
async def setup_boards(setup_sprints: None, transaction_session: AsyncSession, boards: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Board, boards)

@pytest_asyncio.fixture
async def setup_columns(setup_boards: None, transaction_session: AsyncSession, columns: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Column, columns)

@pytest_asyncio.fixture
async def setup_tasks(setup_columns: None, transaction_session: AsyncSession, tasks: tuple[dict]) -> None:
    await bulk_save_models(transaction_session, Task, tasks)

@pytest_asyncio.fixture
def get_users(transaction_session: AsyncSession) -> Callable[..., Awaitable[Any]]:
    async def _get_users() -> Sequence[User]:
        res: Result = await transaction_session.execute(select(User))
        return res.scalars().all()
    return _get_users

@pytest.fixture
def users() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.USERS)

@pytest.fixture
def groups() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.GROUPS)

@pytest.fixture
def sprints() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.SPRINTS)

@pytest.fixture
def boards() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.BOARDS)

@pytest.fixture
def columns() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.COLUMNS)

@pytest.fixture
def tasks() -> tuple[dict]:
    return deepcopy(fixtures.db_mocks.TASKS)

@pytest.fixture
def first_group() -> dict:
    return deepcopy(fixtures.db_mocks.GROUPS[0])

@pytest.fixture
def first_sprint() -> dict:
    return deepcopy(fixtures.db_mocks.SPRINTS[0])

@pytest.fixture
def first_board() -> dict:
    return deepcopy(fixtures.db_mocks.BOARDS[0])

@pytest.fixture
def first_column() -> dict:
    return deepcopy(fixtures.db_mocks.COLUMNS[0])

@pytest.fixture
def first_task() -> dict:
    return deepcopy(fixtures.db_mocks.TASKS[0])