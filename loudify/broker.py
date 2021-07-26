"""Broker implementation."""

from . import broker_api
from . import parser


def main(argv=None):
    """Create and start new broker."""

    args = parser.parse_args_broker(argv)
    parser.setup_logging(args.loglevel)

    verbose = False
    if args.loglevel == 10:
        verbose = True
    broker = broker_api.Broker(verbose)
    broker.bind("tcp://*:" + str(args.port))
    broker.mediate()
