"""Client API."""

import logging
import zmq

from . import definitions
from . import zhelpers

# pylint: disable=R0902,E1101,R1705,R0912

_logger = logging.getLogger(__name__)


class Client:
    """Majordomo Protocol Client API Synchronous version.

    Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    broker = None
    ctx = None
    client = None
    poller = None
    timeout = 2500
    verbose = False

    def __init__(self, broker, verbose=False):
        """
        Initialize the client.

        @param broker: address of the broker to connect to
        @param verbose: verbose logging, defaults to False.
        """
        self.broker = broker
        self.verbose = verbose
        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        """Connect or reconnect to broker."""
        if self.client:
            self.poller.unregister(self.client)
            self.client.close()
        self.client = self.ctx.socket(zmq.DEALER)
        self.client.linger = 0
        self.client.connect(self.broker)
        self.poller.register(self.client, zmq.POLLIN)
        if self.verbose:
            _logger.info("I: connecting to broker at %s...", self.broker)

    def send(self, service, request, **flowgraph_vars):
        """
        Send request to broker.

        @param service: service that is requested
        @param request: input data for the request
        @param flowgraph_vars: dict containing all flowgraph values
        @return:
        """
        if not isinstance(request, list):
            request = [request]

        # Prefix request with protocol frames
        # Frame 0: empty (REQ emulation)
        # Frame 1: "MDPCxy" (six bytes, MDP/Client x.y)
        # Frame 2: Service name (printable string)
        if flowgraph_vars:
            request = (
                [b"", definitions.C_CLIENT, service]
                + request
                + [str(flowgraph_vars).encode("ascii")]
            )
        else:
            request = [b"", definitions.C_CLIENT, service] + request

        if self.verbose:
            _logger.info("I: send request to '%s' service: ", service)
            zhelpers.dump(request)
        self.client.send_multipart(request)

    def recv(self):
        """Return the reply message or None if there was no reply."""
        try:
            items = self.poller.poll(self.timeout)
        except KeyboardInterrupt:
            return  # interrupted

        if items:
            # if we got a reply, process it
            msg = self.client.recv_multipart()
            if self.verbose:
                _logger.info("I: received reply:")
                zhelpers.dump(msg)

            if len(msg) < 4:
                _logger.error("E: client msg is to short %s", len(msg))
            empty = msg.pop(0)
            if empty != b"":
                _logger.error("E: client empty msg is not empty %s", empty)
            header = msg.pop(0)
            if definitions.C_CLIENT != header:
                _logger.error("E: Client header is incorrect %s", header)

            # service = msg.pop(0)
            return msg
        else:
            _logger.warning("W: permanent error, abandoning request")
            return -1
