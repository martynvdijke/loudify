"""CLi interface to connect to the broker."""

import sys
from . import client_sync_api
from . import parser


def main(argv=None):
    """
    Main function for cli to query the system.

    Args:
        Addres: broker addres to connect to
        Port: port to connect to
    Returns:
        None
    """
    args = parser.parse_args_cli(argv)
    parser.setup_logging(args.loglevel)
    verbose = False
    if args.loglevel == 10:
        verbose = True
    print("Runing cli")
    print(args.address, args.port)

    client = client_sync_api.Client("tcp://" + args.address + ":" + str(args.port), verbose)

    request = b"echo"
    reply = client.send(b"mmi.service", request)
    if reply:
        replycode = reply[0]
        print("Lookup echo service:", replycode)
    else:
        print("E: no response from broker, make sure it's running")


if __name__ == '__main__':
    main()
