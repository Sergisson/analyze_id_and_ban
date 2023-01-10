from logging import Logger

from src.settings.suspicion import SuspicionSettings
from src.repositories.suspicion import SuspicionRepository
from src.repositories.transport_to_analyzer import TransportToAnalyzerRepository


async def get_user_suspicion_usecase(
    id_: str,
    suspicion: SuspicionRepository,
    transport_to_analyzer: TransportToAnalyzerRepository,
    logger: Logger,
) -> int:
    level = await suspicion.get(
        id_=id_,
        logger=logger,
    )
    if level is not None:
        return level
    else:
        # Send id for check analize algorithms
        await transport_to_analyzer.send_id_for_check(
            id_=id_,
            logger=logger,
        )
        # We can't find record => user did't suspicion before
        return 0


async def increment_suspicion_usecase(
    id_: str,
    level: int,
    suspicion: SuspicionRepository,
    suspicion_settings: SuspicionSettings,
    logger: Logger,
) -> bool:
    # Race condition, it is okay
    status = True
    if not await suspicion.increment_value(
        id_=id_,
        level=level,
        logger=logger,
    ):
        status = False
    if not await suspicion.set_expired_time(
        id_=id_,
        expired_time=suspicion_settings.expired_time_in_second,
        logger=logger,
    ):
        status = False
    return status
