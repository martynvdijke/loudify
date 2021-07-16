"""Client cli."""

import sys
from . import client_api


def main():
    """
    Main function for cli client.

    Args:
        Addres:
    Returns:
        None
    """
    verbose = "-v" in sys.argv
    client = client_api.Client("tcp://oracle2.vandijke.xyz:5555", verbose)
    print(client)
    # requests = 10
    # request = None
    # with open("data.txt", "rb") as file:
    #     request = file.read()
    #
    # for i in range(requests):
    #     # request = b"Hello world"
    #     try:
    #         client.send(b"echo", request)
    #     except KeyboardInterrupt:
    #         print("send interrupted, aborting")
    #         return
    #
    # count = 0
    # while count < requests:
    #     try:
    #         reply = client.recv()
    #     except KeyboardInterrupt:
    #         break
    #     else:
    #         # also break on failure to reply:
    #         if reply is None:
    #             break
    #     count += 1
    # print("%i requests/replies processed" % count)


if __name__ == "__main__":
    main()
