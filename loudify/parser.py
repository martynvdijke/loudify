"""Argument parser for all cli parts."""
import logging
import sys
import argparse
import coloredlogs

_logger = logging.getLogger(__name__)


def parse_args_worker(args):
    """Parser for the input arguments.

    Args:
        args: cli arguments given to script

    Returns:
        list of supported arguments

    """
    parser = argparse.ArgumentParser(description="Loudify worker")

    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5555,
        help="Specify the tcp port to bind to [default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--address",
        dest="address",
        type=str,
        default="localhost",
        help="Specify the broker address to connect to[default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-s",
        "--service",
        dest="service",
        type=str,
        default="echo",
        help="Specify the service the worker provides to[default=%(default)r]",
        required=True,
    )
    # set logging level
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def parse_args_broker(args):
    """Parser for the input arguments.

    Args:
        args: cli arguments given to script

    Returns:
        list of supported arguments

    """
    parser = argparse.ArgumentParser(description="Loudify broker")
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5555,
        help="Specify the txp port to bind to [default=%(default)r]",
        required=True,
    )
    # set logging level
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def parse_args_client(args):
    """Parser for the input arguments.

    Args:
        args: cli arguments given to script

    Returns:
        list of supported arguments

    """
    parser = argparse.ArgumentParser(description="Loudify client")
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5555,
        help="Specify the tcp port to bind to [default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--address",
        dest="address",
        type=str,
        default="localhost",
        help="Specify the broker address to connect to[default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-m",
        "--mode",
        dest="mode",
        choices=("sync", "async"),
        default="sync",
        help="Specify the mode to use [default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-n",
        "--requests",
        dest="requests",
        type=int,
        default=2,
        help="Specify the number of request to be made [default=%(default)r]",
    )
    # set logging level
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def parse_args_cli(args):
    """Parser for the input arguments.

    Args:
        args: cli arguments given to script

    Returns:
        list of supported arguments

    """
    parser = argparse.ArgumentParser(description="Loudify client")
    parser.add_argument(
        "-p",
        "--port",
        dest="port",
        type=int,
        default=5555,
        help="Specify the tcp port to bind to [default=%(default)r]",
        required=True,
    )
    parser.add_argument(
        "-a",
        "--address",
        dest="address",
        type=str,
        default="localhost",
        help="Specify the broker address to connect to[default=%(default)r]",
        required=True,
    )
    # set logging level
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )
    return parser.parse_args(args)


def setup_logging(loglevel: str) -> None:
    """
    Setup basic logging functionality.

    Args:
      loglevel (int): minimum loglevel for emitting messages

    Returns:
        None
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel,
        stream=sys.stdout,
        format=logformat,
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    coloredlogs.install(level=loglevel, logger=_logger)
