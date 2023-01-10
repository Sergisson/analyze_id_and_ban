import pytest
from sanic_testing.testing import SanicASGITestClient

from tests.api.data.urls import (
    GET_SUSPICION_URL,
    INCREMENT_SUSPICION_URL,
)
from src.repositories.suspicion import RedisRepository
from tests.api.data.response_data.get_suspicion import (
    GET_SUSPICION_SUCCESS_20,
    GET_SUSPICION_SUCCESS_60,
)
from tests.api.data.response_data.set_suspicion import (
    INCREMENT_SUSPICION_SUCCESS,
    INCREMENT_SUSPICION_WITHOUT_ID,
    INCREMENT_SUSPICION_WITHOUT_SUSPICION,
)


@pytest.mark.asyncio
async def test_increment_suspicion_success_20(
    asgi_client: SanicASGITestClient,
    redis_client: RedisRepository,
):
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1", "suspicion": 20},
    )
    assert response.status_code == 200
    assert response.json == INCREMENT_SUSPICION_SUCCESS

    await redis_client.set(
        id_="1",
        suspicion=0,
        expired_time_in_second=1,
        logger=redis_client.logger,
    )


@pytest.mark.asyncio
async def test_set_and_get_suspicion_success_20(
    asgi_client: SanicASGITestClient,
    redis_client: RedisRepository,
):
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1", "suspicion": 20},
    )
    assert response.status_code == 200
    assert response.json == INCREMENT_SUSPICION_SUCCESS

    _, response = await asgi_client.get(url=GET_SUSPICION_URL, params={"id": 1})
    assert response.status_code == 200
    assert response.json == GET_SUSPICION_SUCCESS_20

    await redis_client.set(
        id_="1",
        suspicion=0,
        expired_time_in_second=1,
        logger=redis_client.logger,
    )


@pytest.mark.asyncio
async def test_increment_suspicion_success_3_times_60(
    asgi_client: SanicASGITestClient,
    redis_client: RedisRepository,
):
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1", "suspicion": 20},
    )
    assert response.status_code == 200
    assert response.json == INCREMENT_SUSPICION_SUCCESS
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1", "suspicion": 10},
    )
    assert response.status_code == 200
    assert response.json == INCREMENT_SUSPICION_SUCCESS
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1", "suspicion": 30},
    )
    assert response.status_code == 200
    assert response.json == INCREMENT_SUSPICION_SUCCESS

    _, response = await asgi_client.get(url=GET_SUSPICION_URL, params={"id": 1})
    assert response.status_code == 200
    assert response.json == GET_SUSPICION_SUCCESS_60

    await redis_client.set(
        id_="1",
        suspicion=0,
        expired_time_in_second=1,
        logger=redis_client.logger,
    )


@pytest.mark.asyncio
async def test_increment_suspicion_failed_without_id(
    asgi_client: SanicASGITestClient,
    redis_client: RedisRepository,
):
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"suspicion": 20},
    )
    assert response.status_code == 500
    assert response.json == INCREMENT_SUSPICION_WITHOUT_ID

    await redis_client.set(
        id_="1",
        suspicion=0,
        expired_time_in_second=1,
        logger=redis_client.logger,
    )


@pytest.mark.asyncio
async def test_increment_suspicion_failed_without_suspicion(
    asgi_client: SanicASGITestClient,
    redis_client: RedisRepository,
):
    _, response = await asgi_client.post(
        url=INCREMENT_SUSPICION_URL,
        json={"id": "1"},
    )
    assert response.status_code == 500
    assert response.json == INCREMENT_SUSPICION_WITHOUT_SUSPICION

    await redis_client.set(
        id_="1",
        suspicion=0,
        expired_time_in_second=1,
        logger=redis_client.logger,
    )
