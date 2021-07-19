"""Worker class for the Broker."""

import time


class Worker:
    """A Worker for the Broker, idle or active."""

    identity = None  # hex Identity of worker
    address = None  # Address to route to
    service = None  # Owning service, if known
    expiry = None  # expires at this point, unless heartbeat

    def __init__(self, identity, address, lifetime):
        """Generate a worker entity for the Broker.

        Args:
            identity ([type]): unique worker identity
            address ([type]): hexily addres of the worker
            lifetime ([timedelta]): lifetime the worker can be conntected to the broker
        """
        self.identity = identity
        self.address = address
        self.expiry = time.time() + 1e-3 * lifetime
