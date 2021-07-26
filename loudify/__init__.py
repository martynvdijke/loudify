"""Initialisation module for loudify broker."""
import logging

from setuptools_scm import get_version

from . import broker
from . import parser
from . import worker
from . import client
from . import cli

__author__ = "Martyn van Dijke"
__copyright__ = "Martyn van Dijke"
__license__ = "MIT"
try:
    __version__ = get_version(version_scheme="post-release", local_scheme="no-local-version")
except LookupError:
    __version__ = "0.0"

_logger = logging.getLogger(__name__)


def main_worker(argv=None) -> None:
    """
    Main function of loudify worker.

    Args:
        argv: sys arguments

    Returns:
        none
    """
    args = parser.parse_args_worker(argv)
    parser.setup_logging(args.loglevel)
    _logger.info("Started cli loudify worker version %s", __version__)
    worker.main()


def main_broker(argv=None) -> None:
    """
    Main function of loudify broker cli.

    Args:
        argv: sys arguments

    Returns:
        none
    """
    args = parser.parse_args_broker(argv)
    parser.setup_logging(args.loglevel)
    _logger.info("Started loudify broker version %s", __version__)
    broker.main()


def main_client(argv=None) -> None:
    """
    Main function of loudify worker cli.

    Args:
        argv: sys arguments

    Returns:
        none
    """
    args = parser.parse_args_client(argv)
    parser.setup_logging(args.loglevel)
    _logger.info("Started loudify client version %s", __version__)
    client.main()


def main_cli(argv=None) -> None:
    """
    Main function of loudify cli interface.

    Args:
        argv: sys arguments

    Returns:
        none
    """
    args = parser.parse_args_cli(argv)
    parser.setup_logging(args.loglevel)
    _logger.info("Started loudify cli interface version %s", __version__)
    cli.main()
