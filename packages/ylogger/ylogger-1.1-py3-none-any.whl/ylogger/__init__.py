import logging
from logging import config as logging_config

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters":
        {
            "default": {
                "format": "%(asctime)s  %(filename)s:%(lineno)3d | %(levelname)s  %(message)s"
            },
            "root": {
                "format": "ROOT- %(asctime)s  %(filename)s:%(lineno)3d | %(levelname)s  %(message)s"
            }
        },
    "handlers":
        {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default"
            },
            "root_console": {
                "class": "logging.StreamHandler",
                "formatter": "root"
            }
        },
    "loggers":
        {
            "app":
                {
                    "handlers": ["console"],
                    "level": "INFO",
                    # Don't send it up my namespace for additional handling
                    "propagate": False
                }
        },
    "root": {
        "handlers": ["root_console"],
        "level": "INFO"
    }
}

logging_config.dictConfig(LOGGING_CONFIG)
Logger = logging.getLogger('app')
