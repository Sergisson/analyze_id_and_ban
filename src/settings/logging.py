from sanic.log import LOGGING_CONFIG_DEFAULTS


LOGGING_FORMAT = (
    "%(asctime)s - (%(name)s)[%(levelname)s][%(host)s]: "
    "%(request)s %(message)s %(status)d %(byte)d"
)

LOGGING_CONFIG = LOGGING_CONFIG_DEFAULTS
LOGGING_CONFIG["formatters"]["access"]["format"] = LOGGING_FORMAT
