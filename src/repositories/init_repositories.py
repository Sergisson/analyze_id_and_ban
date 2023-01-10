from logging import Logger
from dataclasses import dataclass

from src.settings import Settings
from src.repositories.suspicion import (
    RedisRepository,
    SuspicionRepository,
)
from src.repositories.transport_to_analyzer import (
    RabbitMQRepository,
    TransportToAnalyzerRepository,
)


@dataclass
class Repositories:
    suspicion: SuspicionRepository
    transport_to_analyzer: TransportToAnalyzerRepository

    @classmethod
    def instantiate(
        cls,
        settings: Settings,
        logger: Logger,
    ):
        return cls(
            suspicion=RedisRepository(
                redis_settings=settings.redis,
                logger=logger,
            ),
            transport_to_analyzer=RabbitMQRepository(settings.rabbit_mq),
        )
