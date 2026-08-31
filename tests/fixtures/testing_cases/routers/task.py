from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_204_NO_CONTENT

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase

TEST_TASK_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'Задача №3',
            'description': 'Выполнить разработку Redis',
            'author_id': 'd66e86ca-a56f-41af-a2c6-b946fb9def2a',
            'observers_ids': [
                'f447b29d-8e56-4b07-9f53-8add7e10e9cf'
            ],
            'column_id': '2c211c90-8560-4a62-97cf-b4fec1e8adfd',
            'board_id': '2b746b59-7c63-4852-a9a5-77caf4699eae',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'title': 'Задача №3',
            'description': 'Выполнить разработку Redis',
            'author_id': 'd66e86ca-a56f-41af-a2c6-b946fb9def2a',
            'observers_ids': [
                'f447b29d-8e56-4b07-9f53-8add7e10e9cf'
            ],
            'column_id': '2c211c90-8560-4a62-97cf-b4fec1e8adfd',
            'board_id': '2b746b59-7c63-4852-a9a5-77caf4699eae',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/',
        headers={},
        data={
            'title': 'Задача №2',
            'description': 'Выполнить тестирование',
            'author_id': '00000000-0000-0000-0000-000000000000',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Non-existent author',
    ),
]

TEST_TASK_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'title': 'Задача №1',
            'description': 'Выполнить разработку',
            'author_id': 'd66e86ca-a56f-41af-a2c6-b946fb9def2a',
            'id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'observers_ids': [
                'f447b29d-8e56-4b07-9f53-8add7e10e9cf'
            ],
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/1',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid task id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent task',
    ),
]

TEST_TASK_ROUTE_UPDATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        data={
            'title': 'Задача №1 (Обновлённая)',
            'description': 'Обновлённое описание задачи.',
        },
        expected_status=HTTP_200_OK,
        expected_data={
            'title': 'Задача №1 (Обновлённая)',
            'description': 'Обновлённое описание задачи.',
            'author_id': 'd66e86ca-a56f-41af-a2c6-b946fb9def2a',
            'id': '3d3e784f-646a-4ad4-979c-dca5dcea2a28',
            'observers_ids': [
                'f447b29d-8e56-4b07-9f53-8add7e10e9cf'
            ],
        },
        description='Positive case for updating task',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/1',
        headers={},
        data={
            'title': 'Задача №1',
            'description': 'Описание задачи.',
        },
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Update non-existent task',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body for update',
    ),
]

TEST_TASK_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/3d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_204_NO_CONTENT,
        expected_data={},
        description='Positive case for deleting task',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/tasks/1',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Delete non-existent task',
    ),
]