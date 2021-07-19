"""Client cli."""

import sys
from . import client_api
from . import parser


def main(argv=None):
    """
    Main function for cli client.

    Args:
        Addres:
    Returns:
        None
    """
    args = parser.parse_args_client(argv)
    parser.setup_logging(args.loglevel)
    verbose = False
    if args.loglevel == 10:
        verbose = True

    client = client_api.Client("tcp://"+args.address+":"+str(args.port), verbose)

    requests = 10

    for i in range(requests):
        request = b"Hello world"
        try:
            client.send(b"echo",  request)
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
