from dataclasses import dataclass

from environs import Env


@dataclass
class ApplicationSettings:
    host: str
    port: int

    @classmethod
    def instantiate(cls):
        env = Env()

        return cls(
            host=env.str("APP_HOST"),
            port=env.int("APP_PORT"),
        )
