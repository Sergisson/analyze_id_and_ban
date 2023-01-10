import pytest as pytest
from sanic.log import logger
from sanic_testing.testing import SanicASGITestClient

from src.settings import Settings
from src.http_app.app import create_app
from src.settings.suspicion import (
    RedisSettings,
    SuspicionSettings,
)
from src.settings.application import ApplicationSettings
from src.repositories.suspicion import RedisRepository
from src.settings.analize_algorithms import RabbitMQSettings


def get_redis_setting() -> RedisSettings:
    return RedisSettings(
        host="127.0.0.1",
        port=6379,
        db_name=2,
        password="redis_password",
    )


def get_suspicion_settings() -> SuspicionSettings:
    return SuspicionSettings(
        expired_time_in_second=1000,
    )


def get_rabbit_mq_settings() -> RabbitMQSettings:
    return RabbitMQSettings(
        host="localhost",
        port=5672,
        user="rabbit_mq_user",
        password="rabbit_mq_user_password",
        routing_key="test_rabbit_mq_routing_key",
    )


def get_application_settings() -> ApplicationSettings:
    return ApplicationSettings(
        host="0.0.0.0",
        port=8000,
    )


def get_test_settings() -> Settings:
    return Settings(
        redis=get_redis_setting(),
        suspicion=get_suspicion_settings(),
        rabbit_mq=get_rabbit_mq_settings(),
        application=get_application_settings(),
    )


@pytest.fixture
def asgi_client() -> SanicASGITestClient:
    settings = get_test_settings()
    sanic_app = create_app(settings=settings)
    return sanic_app.asgi_client


@pytest.fixture
def redis_client() -> RedisRepository:
    return RedisRepository(
        redis_settings=get_redis_setting(),
        logger=logger,
    )
