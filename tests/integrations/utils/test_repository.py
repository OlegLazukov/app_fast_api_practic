import logging
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.models import User, Task, Group
from src.utils.custom_types import AsyncFunc
from src.utils.repository import SqlAlchemyRepository
from tests.fixtures import testing_cases
from tests.utils import BaseTestCase, compare_dicts_and_db_models

if TYPE_CHECKING:
    from collections.abc import Sequence

logging.basicConfig()

class TestSqlAlchemyRepository:
    class _SqlAlchemyRepository(SqlAlchemyRepository):
        _model = Task

    def __get_sql_rep(self, session: AsyncSession) -> SqlAlchemyRepository:
        return self._SqlAlchemyRepository(session)

    @pytest.mark.usefixtures('setup_tasks')
    async def test_add_one(
        self,
        transaction_session: AsyncSession,
        first_task: dict,
        get_tasks: AsyncFunc,
    ) -> None:
        try:
            sql_rep = self.__get_sql_rep(transaction_session)
            await sql_rep.add_one(**first_task)
            await transaction_session.flush()

            tasks_in_db: Sequence[User] = await get_tasks()
            assert compare_dicts_and_db_models(tasks_in_db, [first_task], Task)
        except Exception as e:
            print(e)

    @pytest.mark.usefixtures('setup_tasks')
    async def test_add_one_and_get_id(
        self,
        transaction_session: AsyncSession,
        first_task: dict,
        get_tasks: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        task_id = await sql_rep.add_one_and_get_id(**first_task)
        assert task_id == first_task.get('id')
        await transaction_session.flush()

        tasks_in_db: Sequence[User] = await get_tasks()
        assert compare_dicts_and_db_models(tasks_in_db, [first_task], Task)

    @pytest.mark.usefixtures('setup_tasks')
    async def test_add_one_and_get_obj(
        self,
        transaction_session: AsyncSession,
        first_task: dict,
        get_tasks: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        task = await sql_rep.add_one_and_get_obj(**first_task)
        assert task.id == first_task.get('id')
        await transaction_session.flush()

        task_in_db: Sequence[User] = await get_tasks()
        assert compare_dicts_and_db_models(task_in_db, [first_task], Task)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ONE_OR_NONE_PARAMS)
    async def test_get_by_filter_one_or_none(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            group_in_db: Group | None = await sql_rep.get_by_filter_one_or_none(**case.data)  # Пример для группы
            result = None if not group_in_db else group_in_db.to_schema()
            assert result == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_GET_BY_QUERY_ALL_PARAMS)
    async def test_get_by_filter_all(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            groups_in_db: Sequence[Group] = await sql_rep.get_by_filter_all(**case.data)
            assert compare_dicts_and_db_models(groups_in_db, case.expected_data, Group)

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_UPDATE_ONE_BY_ID_PARAMS)
    async def test_update_one_by_id(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        with case.expected_error:
            updated_group: Group | None = await sql_rep.update_one_by_id(case.data.pop('_id'), **case.data)  # Обновление данных группы
            assert updated_group.to_schema() == case.expected_data

    @pytest.mark.usefixtures('setup_users')
    @pytest.mark.parametrize('case', testing_cases.TEST_SQLALCHEMY_REPOSITORY_DELETE_BY_QUERY_PARAMS)
    async def test_delete_by_filter(
        self,
        case: BaseTestCase,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        try:
            sql_rep = self.__get_sql_rep(transaction_session)
            with case.expected_error:
                await sql_rep.delete_by_filter(**case.data)
                await transaction_session.flush()
                groups_in_db: Sequence[Group] = await get_users()
                assert compare_dicts_and_db_models(groups_in_db, case.expected_data, Group)
        except Exception as e:
            print(e)

    @pytest.mark.usefixtures('setup_users')
    async def test_delete_all(
        self,
        transaction_session: AsyncSession,
        get_users: AsyncFunc,
    ) -> None:
        sql_rep = self.__get_sql_rep(transaction_session)
        await sql_rep.delete_all()
        await transaction_session.flush()
        groups_in_db: Sequence[Group] = await get_users()
        assert groups_in_db == []