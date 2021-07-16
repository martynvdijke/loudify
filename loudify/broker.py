"""Broker implementation."""

import sys
from . import broker_api


def main():
    """Create and start new broker."""
    verbose = "-v" in sys.argv
    broker = broker_api.Broker(verbose)
    broker.bind("tcp://*:5555")
    broker.mediate()
