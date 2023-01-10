import pytest

from tests.api.data.urls import GET_SUSPICION_URL
from tests.api.data.response_data.get_suspicion import (
    GET_SUSPICION_SUCCESS_0,
    GET_SUSPICION_FAILED_WITHOUT_ID_RESPONSE,
)


@pytest.mark.asyncio
async def test_get_suspicion_success_0(asgi_client):
    _, response = await asgi_client.get(url=GET_SUSPICION_URL, params={"id": 1})
    assert response.status_code == 200
    assert response.json == GET_SUSPICION_SUCCESS_0


@pytest.mark.asyncio
async def test_get_suspicion_failed_without_id(asgi_client):
    _, response = await asgi_client.get(url=GET_SUSPICION_URL)
    assert response.status_code == 500
    assert response.json == GET_SUSPICION_FAILED_WITHOUT_ID_RESPONSE
