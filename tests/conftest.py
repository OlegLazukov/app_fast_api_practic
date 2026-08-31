import asyncio
from collections.abc import AsyncGenerator

import pytest
import pytest_asyncio
import sqlalchemy
from httpx import AsyncClient, ASGITransport
from sqlalchemy import Result, sql
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine
from src.config import settings
from src.main import app
from src.models.models import Base
from src.utils.unit_of_work import UnitOfWork
from tests.fixtures import FakeUnitOfWork


@pytest.fixture(scope='session')
def event_loop(request: pytest.FixtureRequest) -> asyncio.AbstractEventLoop:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def create_test_db(event_loop: None) -> None:
    assert settings.MODE == 'TEST'

    sqlalchemy_database_url = (
        f'postgresql+asyncpg://{settings.DB_USER}:{settings.DB_PASS}'
        f'@{settings.DB_HOST}:{settings.DB_PORT}/'
    )
    nodb_engine = create_async_engine(
        sqlalchemy_database_url,
        echo=True,
        future=True,
    )
    db = AsyncSession(bind=nodb_engine)

    db_exists_query = sql.text(f"SELECT 1 FROM pg_catalog.pg_database WHERE datname = '{settings.DB_NAME}'")
    db_exists: Result = await db.execute(db_exists_query)
    db_exists = db_exists.fetchone() is not None
    autocommit_engine = nodb_engine.execution_options(isolation_level='AUTOCOMMIT')
    connection = await autocommit_engine.connect()
    if not db_exists:
        db_create_query = sql.text(f'CREATE DATABASE {settings.DB_NAME}')
        await connection.execute(db_create_query)

    yield

    db_drop_query = sql.text(f'DROP DATABASE IF EXISTS {settings.DB_NAME} WITH (FORCE)')
    await db.close()
    await connection.execute(db_drop_query)
    await connection.close()
    await nodb_engine.dispose()


@pytest_asyncio.fixture(scope='session')
async def db_engine(create_test_db: None) -> AsyncGenerator[AsyncEngine, None]:
    engine = create_async_engine(
        settings.DB_URL,
        echo=False,
        future=True,
        pool_size=50,
        max_overflow=100,
    ).execution_options(compiled_cache=None)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_schemas(db_engine: AsyncEngine) -> None:
    assert settings.MODE == 'TEST'

    schemas = (
        'schema_for_example',
    )

    async with db_engine.connect() as conn:
        for schema in schemas:
            await conn.execute(sqlalchemy.schema.CreateSchema(schema))
            await conn.commit()


@pytest_asyncio.fixture(scope='session', autouse=True)
async def setup_db(db_engine: AsyncEngine, setup_schemas: None) -> None:

    assert settings.MODE == 'TEST'

    async with db_engine.begin() as db_conn:
        await db_conn.run_sync(Base.metadata.drop_all)
        await db_conn.run_sync(Base.metadata.create_all)


@pytest_asyncio.fixture
async def transaction_session(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession, None]:
    connection = await db_engine.connect()
    await connection.begin()
    session = AsyncSession(bind=connection)

    yield session

    await session.rollback()
    await connection.close()


@pytest_asyncio.fixture
def fake_uow(transaction_session: AsyncSession) -> FakeUnitOfWork:
    _fake_uow = FakeUnitOfWork(transaction_session)
    yield _fake_uow


@pytest_asyncio.fixture
async def async_client(fake_uow: FakeUnitOfWork) -> AsyncGenerator[AsyncClient, None]:
    app.dependency_overrides[UnitOfWork] = lambda: fake_uow
    async with AsyncClient(transport=ASGITransport(app=app), base_url='http://test') as ac:
        yield ac