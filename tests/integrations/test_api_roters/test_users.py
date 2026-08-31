import pytest
from httpx import AsyncClient

from tests.conftest import async_client
from tests.fixtures import testing_cases
from tests.utils import RequestTestCase, prepare_payload



class TestTaskRouter:
    @staticmethod
    @pytest.mark.parametrize("case", testing_cases.TEST_USER_ROUTE_CREATE_PARAMS)
    async def test_create_user(
            case: RequestTestCase,
            async_client: AsyncClient
    ) -> None:
        with case.expected_error:
            response = await async_client.post(
                case.url,
                json=case.data,
                headers=case.headers
            )
            assert response.status_code == case.expected_status
            assert prepare_payload(response, ['id']) == case.expected_data

    @staticmethod
    @pytest.mark.parametrize("case", testing_cases.TEST_USER_ROUTE_GET_PARAMS)
    async def test_get_users(
            case: RequestTestCase,
            async_client: AsyncClient
    ) -> None:
        with case.expected_error:
            response = await async_client.get(
                case.url,
                headers=case.headers,
            )
            assert response.status_code == case.expected_status
            assert prepare_payload(response) == case.expected_data


    @staticmethod
    @pytest.mark.parametrize("case", testing_cases.TEST_USER_ROUTE_UPDATE_PARAMS)
    async def test_update_user(
            case: RequestTestCase,
            async_client: AsyncClient
    ) -> None:
        with case.expected_error:
            response = await async_client.put(
                case.url,
                json=case.data,
                headers=case.headers
            )
            assert response.status_code == case.expected_status
            assert prepare_payload(response) == case.expected_data


    @staticmethod
    @pytest.mark.parametrize("case", testing_cases.TEST_USER_ROUTE_DELETE_PARAMS)
    async def test_delete_user(
            case: RequestTestCase,
            async_client: AsyncClient
    ) -> None:
        with case.expected_error:
            response = await async_client.delete(
                case.url,
                headers=case.headers
            )
            assert response.status_code == case.expected_status
            assert prepare_payload(response) == case.expected_data