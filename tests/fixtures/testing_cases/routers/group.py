from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase


TEST_GROUP_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/groups/',
        headers={},
        data={
            'name': 'Новая группа',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'id': str,
            'name': 'Новая группа',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/groups/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
]

TEST_GROUP_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/groups/e5e4c2ef-f27f-4dcd-b940-becf0ecac144',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': str,
            'name': 'Группа 1',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/groups/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid group id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/groups/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent group',
    ),
]