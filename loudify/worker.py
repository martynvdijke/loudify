"""Actual Loudify worker."""


import sys
from . import worker_api
from . import parser


def main(argv=None):
    """
    Main function.

    Args:
        Addres:
    Returns:
        None
    """
    args = parser.parse_args_worker(argv)
    parser.setup_logging(args.loglevel)

    verbose = False
    if args.loglevel == 10:
        verbose = True

    worker = worker_api.Worker("tcp://"+args.address+":"+str(args.port), str(args.service).encode(), verbose)
    reply = None
    while True:
        request = worker.recv(reply)
        if request is None:
            break  # Worker was interrupted
        reply = request  # Echo is complex... :-)


if __name__ == "__main__":
    main()
