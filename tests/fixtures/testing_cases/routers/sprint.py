from datetime import datetime

from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase


TEST_SPRINT_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/sprints/',
        headers={},
        data={
            'name': 'Новый спринт',
            'start_date': datetime(2023, 2, 1),
            'end_date': datetime(2023, 2, 15),
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'id': str,
            'name': 'Новый спринт',
            'start_date': datetime(2023, 2, 1),
            'end_date': datetime(2023, 2, 15),
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/sprints/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
]

TEST_SPRINT_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/sprints/b3a7db69-fb51-4e92-8f88-f1db4757e81c',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': str,
            'name': 'Спринт 2',
            'start_date': datetime(2023, 2, 1),
            'end_date': datetime(2023, 2, 15),
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/sprints/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid sprint id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/sprints/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent sprint',
    ),
]