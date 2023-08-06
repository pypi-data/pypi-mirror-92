"""
This module is used to interact with the data finance api
"""
import logging
from . import exceptions
from .client import DfClient

__all__ = ["DfClient"]
__version__ = "0.0.1"

logging.getLogger(__name__).addHandler(logging.NullHandler())

