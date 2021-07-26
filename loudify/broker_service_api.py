"""Service class for the Broker."""

# pylint: disable=R0205,R0903


class Service:
    """A single Service."""

    name = None  # Service name
    requests = None  # List of client requests
    waiting = None  # List of waiting workers

    def __init__(self, name):
        """
        Initialize a service.

        @param name: service name
        """
        self.name = name
        self.requests = []
        self.waiting = []
