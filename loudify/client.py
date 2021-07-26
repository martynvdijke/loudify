"""Async Client cli."""

from . import client_async_api
from . import client_sync_api
from . import parser


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

    client = client_async_api.Client("tcp://" + args.address + ":" + str(args.port), verbose)

    requests = 10
    flowgraph_vars= {'sf': 7, 'samp_rate': 250000, 'bw': 250000, 'has_crc': False, 'pay_len': 64, 'cr': 4, 'impl_head': True, 'sync_words': [
        8, 16]}

    for i in range(requests):
        request = b"Hello world"
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
    # print("%i requests/replies processed" % count)


if __name__ == "__main__":
    main()
