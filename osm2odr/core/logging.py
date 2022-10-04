import logging
from logging.config import dictConfig

from pydantic import BaseModel


class LogConfig(BaseModel):
    LOGGER_NAME: str = "osm2odr"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_LEVEL: str = "INFO"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
    handlers = {
        "default": {
            "formatter": "default",
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stderr",
        },
    }
    loggers = {
        "osm2odr": {"handlers": ["default"], "level": LOG_LEVEL}
    }


dictConfig(LogConfig().dict())
log = logging.getLogger("osm2odr")
