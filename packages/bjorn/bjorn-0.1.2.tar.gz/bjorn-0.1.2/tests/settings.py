import os

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {"format": "%(asctime)s [%(levelname)s] %(name)s: "
                               "%(message)s"},
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "formatter": "standard",
            "class": "logging.StreamHandler",
        },
        "file_handler": {
            "level": "INFO",
            "filename": "/tmp/mylogfile.log",
            "class": "logging.FileHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "job": {
            "handlers": ["default"],
            "level": os.environ.get("LOGGER_LEVEL", "INFO"),
            "propagate": True,
        },
    },
}

VALUE_TO_TEST = "A"
