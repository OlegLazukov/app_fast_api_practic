from datetime import datetime

import pytest
from uuid import UUID, uuid4
from sqlalchemy.exc import MultipleResultsFound
from src.schemas.task import TaskResponse
from src.schemas.user import UserDB
from src.utils.constants import TASK_NOT_FOUND_MSG
from tests.fixtures.db_mocks import TASKS
from tests.utils import BaseTestCase

TEST_BASE_SERVICE_GET_BY_QUERY_ONE_OR_NONE_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'title': 'Задача №1'},
        expected_data=TaskResponse(
        id=UUID('d66e86ca-a56f-41af-a2c6-b946fb9def2a'),
         title='Задача №1',
         description='Выполнить разработку',
         author=UserDB(
             id=UUID('d66e86ca-a56f-41af-a2c6-b946fb9def2a'),
             full_name='Имя Автора 1',
             email='author1@example.com'
         ),
         observers=[UserDB(
             id=UUID('f447b29d-8e56-4b07-9f53-8add7e10e9cf'),
             full_name='Имя Исполнителя 2',
             email='executor2@example.com'
         )],
         column_id=UUID('2c211c90-8560-4a62-97cf-b4fec1e8adfd'),
         board_id=UUID('2b746b59-7c63-4852-a9a5-77caf4699eae'),
         sprint_id=None,
         group_id=None,
         status="todo",
         created_at=datetime.now()
        ),
    ),
    BaseTestCase(
        data={'title': 'Задача №2'},
        expected_data=None,
    ),
    BaseTestCase(
        data={'title': 'Задача №3'},
        expected_data=None,
        expected_error=pytest.raises(MultipleResultsFound),
    ),
]

TEST_BASE_SERVICE_GET_BY_QUERY_ALL_PARAMS: list[BaseTestCase] = [
    BaseTestCase(data={'title': 'Задача №1'}, expected_data=[TASKS[0]]),
    BaseTestCase(data={'title': 'Задача №2'}, expected_data=[]),
    BaseTestCase(data={'title': 'Задача №3'}, expected_data=TASK_NOT_FOUND_MSG),
]

TEST_BASE_SERVICE_UPDATE_ONE_BY_ID_PARAMS: list[BaseTestCase] = [
    BaseTestCase(
        data={'_id': TASKS[0]['id'], 'title': 'Задача Обновленная'},
        expected_data=TaskResponse(
            id=UUID('b04e55bd-8431-4edd-8eb4-632099c0ea65'),
            title='Задача Обновленная',
            description='Выполнить разработку',
            author=UserDB(
                id=UUID('d66e86ca-a56f-41af-a2c6-b946fb9def2a'),
                full_name='Имя Автора 1',
                email='author1@example.com'
            ),
            observers=[UserDB(
                id=UUID('f447b29d-8e56-4b07-9f53-8add7e10e9cf'),
                full_name='Имя Исполнителя 2',
                email='executor2@example.com'
            )],
            column_id=UUID('2c211c90-8560-4a62-97cf-b4fec1e8adfd'),
            board_id=UUID('2b746b59-7c63-4852-a9a5-77caf4699eae'),
            sprint_id=None,
            group_id=None,
            status='in_progress',
            created_at=datetime.now()
        ),
    ),
]

TEST_BASE_SERVICE_DELETE_BY_QUERY_PARAMS: list[BaseTestCase] = [
    BaseTestCase(data={'id': TASKS[0]['id']}, expected_data=TASKS[1:]),
    BaseTestCase(data={'title': 'Задача №2'}, expected_data=[TASKS[1]]),
    BaseTestCase(data={'id': uuid4()}, expected_data=TASKS),
    BaseTestCase(data={}, expected_data=[]),
]