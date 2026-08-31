from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase


TEST_BOARD_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/boards/',
        headers={},
        data={
            'name': 'Доска проекта 3',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'id': str,
            'name': 'Доска проекта 3',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/boards/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
]

TEST_BOARD_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/boards/a140cab8-0e98-42e5-b921-9c41fe480b0a',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': str,
            'name': 'Доска проекта 2',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/boards/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid board id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/boards/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent board',
    ),
]