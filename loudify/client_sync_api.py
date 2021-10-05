"""Synchronus Client API."""

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
    timeout = 25000
    retries = 3
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
        self.client = self.ctx.socket(zmq.REQ)
        self.client.linger = 0
        self.client.connect(self.broker)
        self.poller.register(self.client, zmq.POLLIN)
        if self.verbose:
            _logger.info("I: connecting to broker at %s...", self.broker)

    def send(self, service, request, flowgraph_vars=None):
        """
        Send request to broker and get reply by hook or crook.

        Takes ownership of request message and destroys it when sent.
        Returns the reply message or None if there was no reply.

        @param service: service that is requested
        @param request: input data for the request
        @param flowgraph_vars: dict containing all flowgraph values
        @return:
        """

        if not isinstance(request, list):
            request = [request]

        if flowgraph_vars is not None:
            request = (
                [definitions.C_CLIENT, service] + request + [str(flowgraph_vars).encode("ascii")]
            )
        else:
            request = [definitions.C_CLIENT, service] + request

        if self.verbose:
            _logger.info("I: send request to '%s' service: ", service)
            zhelpers.dump(request)
        reply = None

        retries = self.retries
        while retries > 0:
            self.client.send_multipart(request)
            try:
                items = self.poller.poll(self.timeout)
            except KeyboardInterrupt:
                break  # interrupted

            if items:
                msg = self.client.recv_multipart()
                if self.verbose:
                    _logger.info("I: received reply:")
                    zhelpers.dump(msg)

                if len(msg) < 3:
                    _logger.warning("E: client msg is to short %s", len(msg))

                header = msg.pop(0)
                if header != definitions.C_CLIENT:
                    _logger.error("E: Client header is incorrect %s", header)

                reply_service = msg.pop(0)

                if service != reply_service:
                    _logger.warning(
                        "E: worker  reply service not the same as internal service of worker %s",
                        service,
                    )

                reply = msg
                break
            else:
                if retries:
                    logging.warning("W: no reply, reconnecting...")
                    self.reconnect_to_broker()
                else:
                    logging.warning("W: permanent error, abandoning")
                    break
                retries -= 1

        return reply

    def destroy(self):
        self.context.destroy()
