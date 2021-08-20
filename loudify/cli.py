"""CLI interface to connect to the broker."""

import click

from . import client_sync_api
from . import parser
from . import definitions


@click.command()
@click.option(
    "--user_request", type=click.Choice(definitions.internal_commands, case_sensitive=False)
)
def get_choise(user_request):
    """Get user input

    Args:
        user_request ([type]): [description]
    """
    print(user_request)


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
    print("Runing cli interface")
    print(args.address, args.port)

    client = client_sync_api.Client("tcp://" + args.address + ":" + str(args.port), verbose)

    value = get_choise()
    print(value)

    request = b"echo"
    reply = client.send(b"mmi.service", request)
    if reply:
        replycode = reply[0]
        print("Lookup echo service:", replycode)
    else:
        print("E: no response from broker, make sure it's running")


if __name__ == "__main__":
    main()
