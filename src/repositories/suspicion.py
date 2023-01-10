from abc import (
    ABC,
    abstractmethod,
)
from typing import Optional
from logging import Logger

from aioredis import (
    RedisError,
    from_url,
)

from src.settings.suspicion import (
    RedisSettings,
    SuspicionSettings,
)
from src.repositories.exceptions import (
    GetSuspicionError,
    SetSuspicionError,
    SetIncrementBySuspicionError,
)


class SuspicionRepository(ABC):
    @abstractmethod
    async def _get(self, key: str) -> int:
        raise NotImplementedError()

    async def get(
        self,
        id_: str,
        logger: Logger,
    ) -> Optional[int]:
        """
        Get level suspicion
        :raise
            GetSuspicionError: raise exception for get value
        """
        try:
            level = await self._get(key=id_)
        except GetSuspicionError as error:
            logger.error(f"Get suspicion error for id({id_}): {error}")
        else:
            if level:
                logger.info(f"Get suspicion successful for id({id_}): {level}")
                try:
                    return int(level)
                except (ValueError, TypeError) as error:
                    logger.error(f"Can't convert level in int: {error}")
            else:
                logger.info(f"id ({id_}) didn't suspicion before")

    # deprecated
    async def set(
        self,
        id_: str,
        suspicion: int,
        expired_time_in_second: int,
        logger: Logger,
    ) -> bool:
        """
        Set suspicion level
        Returns:
            Result status
        Raises:
            SetSuspicionError: raise exception for set value
        """
        try:
            await self._set(
                key=id_,
                value=suspicion,
                expired_time=expired_time_in_second,
            )
        except SetSuspicionError as error:
            logger.error(f"Set suspicion error for id({id_}): {error}")
            return False
        else:
            logger.info(f"Set suspicion successful for id: {id_}")
            return True

    # deprecated
    @abstractmethod
    async def _set(
        self,
        key: str,
        value: int,
        expired_time: int,
    ):
        raise NotImplementedError()

    async def increment_value(
        self,
        id_: str,
        level: int,
        logger: Logger,
    ) -> bool:
        """
        Increment suspicion level
        Returns:
            Result status
        Raises:
            IncrBySuspicionError: raise exception for set value
        """
        try:
            await self._increment_value(
                key=id_,
                value=level,
            )
        except SetIncrementBySuspicionError as error:
            logger.error(f"Increment suspicion error for id({id_}): {error}")
            return False
        else:
            logger.info(f"Increment suspicion successful for id: {id_}")
            return True

    async def _increment_value(
        self,
        key: str,
        value: int,
    ):
        raise NotImplementedError()

    async def set_expired_time(
        self,
        id_: str,
        expired_time: int,
        logger: Logger,
    ):
        """
        Set expired time for id
        Returns:
            Result status
        Raises:
            IncrBySuspicionError: raise exception for set value
        """
        try:
            await self._set_expired_time(
                key=id_,
                expired_time=expired_time,
            )
        except SetIncrementBySuspicionError as error:
            logger.error(f"Set expired time error for id({id_}): {error}")
            return False
        else:
            logger.info(f"Set expired time suspicion successful for id: {id_}")
            return True

    async def _set_expired_time(
        self,
        key: str,
        expired_time: int,
    ):
        raise NotImplementedError()


class RedisRepository(SuspicionRepository):
    def __init__(
        self,
        redis_settings: RedisSettings,
        logger: Logger,
    ):
        url = (
            f"redis://{redis_settings.host}:"
            f"{redis_settings.port}/{redis_settings.db_name}"
        )
        self.redis = from_url(
            url=url,
            password=redis_settings.password,
            encoding="utf-8",
            decode_responses=True,
        )
        self.logger = logger

    async def _get(self, key: str) -> int:
        try:
            return await self.redis.get(
                key,
            )
        except RedisError as error:
            raise GetSuspicionError(error)

    async def _set(
        self,
        key: str,
        value: int,
        expired_time: int,
    ):
        try:
            await self.redis.set(
                key,
                value,
                ex=expired_time,
            )
        except RedisError as error:
            raise SetSuspicionError(error)

    async def _increment_value(
        self,
        key: str,
        value: int,
    ):
        try:
            await self.redis.incrby(
                name=key,
                amount=value,
            )
        except RedisError as error:
            raise SetIncrementBySuspicionError(error)

    async def _set_expired_time(
        self,
        key: str,
        expired_time: int,
    ):
        try:
            await self.redis.expire(
                name=key,
                time=expired_time,
            )
        except RedisError as error:
            raise SetIncrementBySuspicionError(error)
