from dataclasses import (
    field,
    dataclass,
)

from src.settings.logging import LOGGING_CONFIG
from src.settings.suspicion import (
    RedisSettings,
    SuspicionSettings,
)
from src.settings.application import ApplicationSettings
from src.settings.analize_algorithms import RabbitMQSettings


@dataclass
class Settings:
    redis: RedisSettings
    suspicion: SuspicionSettings
    rabbit_mq: RabbitMQSettings
    application: ApplicationSettings
    logging: dict = field(default_factory=lambda: LOGGING_CONFIG)

    @classmethod
    def instantiate(cls):
        return cls(
            redis=RedisSettings.instantiate(),
            suspicion=SuspicionSettings.instantiate(),
            rabbit_mq=RabbitMQSettings.instantiate(),
            application=ApplicationSettings.instantiate(),
        )
