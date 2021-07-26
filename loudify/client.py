"""Async Client cli."""

import logging
from . import client_async_api
from . import client_sync_api
from . import parser

_logger = logging.getLogger(__name__)

def main(argv=None):
    """
    Main function for cli client.

    Args:
        Addres: broker addres to connect to
        Port: port to connect to
    Returns:
        None
    """
    args = parser.parse_args_client(argv)
    parser.setup_logging(args.loglevel)
    verbose = False
    if args.loglevel == 10:
        verbose = True
    if args.mode == "sync":
        client = client_sync_api.Client("tcp://" + args.address + ":" + str(args.port), verbose)
    else:
        client = client_async_api.Client("tcp://" + args.address + ":" + str(args.port), verbose)

    requests = args.requests

    request = b"Hello world"
    flowgraph_vars= {'sf': 7, 'samp_rate': 250000, 'bw': 250000, 'has_crc': False, 'pay_len': 64, 'cr': 4, 'impl_head': True, 'sync_words': [
        8, 16]}
    if args.mode == "sync":
        for req in range(requests):
            reply = client.send(b"echo",  request, flowgraph_vars)
            if reply:
                _logger.debug("D: Got reply back from broker", reply[0])
            else:
                _logger.warning("E: no response from broker, make sure it's running.")
    else:
        for req in range(requests):
            try:
                client.send(b"echo",  request, flowgraph_vars)
            except KeyboardInterrupt:
                print("send interrupted, aborting")
                return

        count = 0
        while count < requests:
            try:
                reply = client.recv()
            except KeyboardInterrupt:
                break
            else:
                # also break on failure to reply:
                if reply is None:
                    break
            count += 1


if __name__ == "__main__":
    main()
