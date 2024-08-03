import logging
from logging.config import dictConfig
import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "app/logs/app.log")  # Path to the log file

# Define logging configuration
logging_config = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
        "file": {
            "class": "logging.FileHandler",
            "filename": LOG_FILE,  # Path to the log file
            "formatter": "default",
        },
    },
    "root": {
        # Ensure handlers are correctly configured
        "handlers": ["console", "file"],
        "level": LOG_LEVEL,
    },
    "loggers": {
        "uvicorn": {
            "handlers": ["console"],  # Use only console handler for Uvicorn
            "level": "INFO",
        },
        # "app": {  # Your custom logger's name
        #     "handlers": ["console", "file"],
        #     "level": LOG_LEVEL,
        # },
    },
}

# Apply logging configuration
logging.config.dictConfig(logging_config)
