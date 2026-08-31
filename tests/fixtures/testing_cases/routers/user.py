from datetime import datetime
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY, \
    HTTP_204_NO_CONTENT

from tests.constants import BASE_ENDPOINT_URL
from tests.utils import RequestTestCase


TEST_USER_ROUTE_CREATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/',
        headers={},
        data={
            'full_name': 'Имя Автора 2',
            'email': 'author2@example.com',
        },
        expected_status=HTTP_201_CREATED,
        expected_data={
            'id': 'f447b29d-8e56-4b07-9f53-8add7e10e9cd',
            'full_name': 'Имя Автора 2',
            'email': 'author2@example.com',
            'created_at': datetime.now(),
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/',
        headers={},
        data={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid request body',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/',
        headers={},
        data={
            'full_name': '',
            'email': 'invalidemail.com',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Invalid user data',
    ),
]

TEST_USER_ROUTE_GET_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/f447b29d-8e56-4b07-9f53-8add7e10e9cd',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': 'f447b29d-8e56-4b07-9f53-8add7e10e9cd',
            'full_name': 'Имя Исполнителя 1',
            'email': 'executor1@example.com',
        },
        description='Positive case',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/d66e86ca-a56f-41af-a2c6-b946fb9def2a',
        headers={},
        expected_status=HTTP_200_OK,
        expected_data={
            'id': 'd66e86ca-a56f-41af-a2c6-b946fb9def2a',
            'full_name': 'Имя Автора 1',
            'email': 'author1@example.com',
        },
        description='Another existing user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/invalid-id',
        headers={},
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Not valid user id',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/4d3e784f-646a-4ad4-979c-dca5dcea2a28',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Non-existent user',
    ),
]

TEST_USER_ROUTE_UPDATE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/f447b29d-8e56-4b07-9f53-8add7e10e9cd',
        headers={},
        data={
            'full_name': 'Имя Автора Обновлённое',
            'email': 'updated_author2@example.com',
        },
        expected_status=HTTP_200_OK,
        expected_data={
            'id': 'f447b29d-8e56-4b07-9f53-8add7e10e9cd',
            'full_name': 'Имя Автора Обновлённое',
            'email': 'updated_author2@example.com',
            'created_at': datetime.now(),
        },
        description='Positive case for updating user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/d66e86ca-a56f-41af-a2c6-b946fb9def2a',
        headers={},
        data={
            'full_name': 'Имя Автора 1 Обновлённое',
            'email': 'invalidemail',
        },
        expected_status=HTTP_422_UNPROCESSABLE_ENTITY,
        expected_data={},
        description='Invalid email format during update',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/1',
        headers={},
        data={
            'full_name': 'Попытка обновления несуществующего пользователя',
            'email': 'non_exist@example.com',
        },
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Update non-existent user',
    ),
]


TEST_USER_ROUTE_DELETE_PARAMS: list[RequestTestCase] = [
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/f447b29d-8e56-4b07-9f53-8add7e10e9cd',
        headers={},
        expected_status=HTTP_204_NO_CONTENT,
        expected_data={},
        description='Positive case for deleting user',
    ),
    RequestTestCase(
        url=f'{BASE_ENDPOINT_URL}/users/1',
        headers={},
        expected_status=HTTP_404_NOT_FOUND,
        expected_data={},
        description='Delete non-existent user',
    ),
]