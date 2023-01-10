from abc import (
    ABC,
    abstractmethod,
)
from logging import Logger

from aiormq import AMQPError
from aio_pika import (
    Message,
    connect_robust,
)

from src.repositories.exceptions import PublishMessageAnalizyAlgoritmsError
from src.settings.analize_algorithms import RabbitMQSettings


class TransportToAnalyzerRepository(ABC):
    async def send_id_for_check(
        self,
        id_: str,
        logger: Logger,
    ) -> None:
        try:
            await self.send_message(message=id_)
        except PublishMessageAnalizyAlgoritmsError as error:
            logger.error(
                f"Send message to algorithms service error for user_id({id_}): {error}"
            )
        else:
            logger.info(
                f"Send message to algorithms service success for user_id: {id_}"
            )

    @abstractmethod
    async def send_message(self, message: str):
        raise NotImplementedError()


class RabbitMQRepository(TransportToAnalyzerRepository):
    def __init__(self, rabbit_mq_settings: RabbitMQSettings):
        self.connection_url = (
            f"amqp://{rabbit_mq_settings.user}:{rabbit_mq_settings.password}"
            f"@{rabbit_mq_settings.host}:{rabbit_mq_settings.port}"
        )
        self.routing_key = rabbit_mq_settings.routing_key

    async def send_message(self, message: str):
        connection = None
        try:
            connection = await connect_robust(
                url=self.connection_url,
            )
            channel = await connection.channel()

            await channel.default_exchange.publish(
                Message(body=message.encode()),
                routing_key=self.routing_key,
            )
        except (AMQPError, ConnectionError) as error:
            raise PublishMessageAnalizyAlgoritmsError(error)
        finally:
            if connection:
                await connection.close()
