from dataclasses import dataclass

from environs import Env


@dataclass
class SuspicionSettings:
    expired_time_in_second: int

    @classmethod
    def instantiate(cls):
        env = Env()

        return cls(expired_time_in_second=env.int("BAN_EXPIRED_TIME_IN_SECOND"))


@dataclass
class RedisSettings:
    host: str
    port: int
    db_name: int
    password: str

    @classmethod
    def instantiate(cls):
        env = Env()

        return cls(
            host=env.str("REDIS_HOST"),
            port=env.int("REDIS_PORT"),
            db_name=env.int("REDIS_DB_NAME"),
            password=env.str("REDIS_PASSWORD"),
        )
