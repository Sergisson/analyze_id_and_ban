from dataclasses import dataclass

from environs import Env


@dataclass
class RabbitMQSettings:
    host: str
    port: int
    user: str
    password: str

    routing_key: str

    @classmethod
    def instantiate(cls):
        env = Env()

        return cls(
            host=env.str("RABBIT_MQ_HOST"),
            port=env.int("RABBIT_MQ_PORT"),
            user=env.str("RABBIT_MQ_USER"),
            password=env.str("RABBIT_MQ_PASSWORD"),
            routing_key=env.str("RABBIT_MQ_ROUTING_KEY"),
        )
