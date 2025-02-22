"""Logging and error handling for the Flask app."""

import logging
from functools import wraps

from flask import request  # pylint:disable=import-error

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Create a console handler to display logs in the terminal
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create a formatter and set it for the handler
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)  # noqa: E501
ch.setFormatter(formatter)

# Add the handler to the logger
logger.addHandler(ch)


def log_request(func):
    """Log the request made to the endpoint."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(
            "Request made to %s with method %s", request.url, request.method
        )  # noqa: E501
        return func(*args, **kwargs)

    return wrapper
