"""Worker API."""

import logging
import time
import zmq

from . import zhelpers

# MajorDomo protocol constants:
from . import definitions

# pylint: disable=R0902,E1101,R1705,R0912
_logger = logging.getLogger(__name__)


class Worker:
    """Worker API.

    Implements the MDP/Worker spec at http:#rfc.zeromq.org/spec:7.
    """

    HEARTBEAT_LIVENESS = 3  # 3-5 is reasonable
    broker = None
    ctx = None
    service = None

    worker = None  # Socket to broker
    heartbeat_at = 0  # When to send HEARTBEAT (relative to time.time(), so in seconds)
    liveness = 0  # How many attempts left
    heartbeat = 2500  # Heartbeat delay, msecs
    reconnect = 2500  # Reconnect delay, msecs

    # Internal state
    expect_reply = False  # False only at start

    timeout = 2500  # poller timeout
    verbose = False  # Print activity to stdout

    # Return address, if any
    reply_to = None

    def __init__(self, broker, service, verbose=False):
        """
        Initializer the Worker class.

        @param broker:
        @param service:
        @param verbose:
        """

        self.broker = broker
        self.service = service
        self.verbose = verbose
        self.ctx = zmq.Context()
        self.poller = zmq.Poller()
        self.reconnect_to_broker()

    def reconnect_to_broker(self):
        """Connect or reconnect to broker."""
        if self.worker:
            self.poller.unregister(self.worker)
            self.worker.close()
        self.worker = self.ctx.socket(zmq.DEALER)
        self.worker.linger = 0
        self.worker.connect(self.broker)
        self.poller.register(self.worker, zmq.POLLIN)
        if self.verbose:
            _logger.info("I: connecting to broker at %s...", self.broker)

        # Register service with broker
        self.send_to_broker(definitions.W_READY, self.service, [])

        # If liveness hits zero, queue is considered disconnected
        self.liveness = self.HEARTBEAT_LIVENESS
        self.heartbeat_at = time.time() + 1e-3 * self.heartbeat

    def send_to_broker(self, command, option=None, msg=None):
        """
        Send message to broker.

        If no msg is provided, creates one internally

        @param command:
        @param option:
        @param msg:
        @return:
        """

        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]

        if option:
            msg = [option] + msg

        msg = [b"", definitions.W_WORKER, command] + msg
        if self.verbose:
            _logger.info("I: sending %s to broker", command)
            zhelpers.dump(msg)
        self.worker.send_multipart(msg)

    def recv(self, reply=None):
        """
        Send reply, if any, to broker and wait for next request.

        @param reply:
        @return:
        """

        try:
            # Format and send the reply if we were provided one
            if reply is None or reply is self.expect_reply:
                _logger.warning("E: Reply is wrong %s", reply)

            if reply is not None:
                if self.reply_to is None:
                    _logger.error("E: reply address is None, invalid msg")
                reply = [self.reply_to, b""] + reply
                self.send_to_broker(definitions.W_REPLY, msg=reply)
        except KeyboardInterrupt:
            exit(0)

        self.expect_reply = True

        while True:
            # Poll socket for a reply, with timeout
            try:
                items = self.poller.poll(self.timeout)
            except KeyboardInterrupt:
                exit(0)
                _logger.warning("W: interrupt received, killing worker...")
                break  # Interrupted
            if items:
                msg = self.worker.recv_multipart()
                if self.verbose:
                    _logger.info("I: received message from broker: ")
                    zhelpers.dump(msg)

                self.liveness = self.HEARTBEAT_LIVENESS
                # Don't try to handle errors, just assert noisily
                if len(msg) < 3:
                    _logger.warning("E: msg length is invalid")

                empty = msg.pop(0)
                if empty != b"":
                    logging.error("E: invalid empty space in message")

                header = msg.pop(0)
                if header != definitions.W_WORKER:
                    _logger.warning("E: header does not eqaul worker definition")

                command = msg.pop(0)
                if command == definitions.W_REQUEST:
                    # We should pop and save as many addresses as there are
                    # up to a null part, but for now, just save one...
                    self.reply_to = msg.pop(0)
                    # pop empty
                    empty = msg.pop(0)
                    if empty != b"":
                        _logger.warning("E: empty space in msg is not empty, invalid msg")
                    return msg  # We have a request to process
                elif command == definitions.W_HEARTBEAT:
                    # Do nothing for heartbeats
                    pass
                elif command == definitions.W_DISCONNECT:
                    self.reconnect_to_broker()
                else:
                    _logger.error("E: invalid input message: ")
                    zhelpers.dump(msg)

            else:
                self.liveness -= 1
                if self.liveness == 0:
                    if self.verbose:
                        _logger.warning("W: disconnected from broker - retrying...")
                    try:
                        time.sleep(1e-3 * self.reconnect)
                    except KeyboardInterrupt:
                        break
                    self.reconnect_to_broker()

            # Send HEARTBEAT if it's time
            if time.time() > self.heartbeat_at:
                self.send_to_broker(definitions.W_HEARTBEAT)
                self.heartbeat_at = time.time() + 1e-3 * self.heartbeat

        
        return None

    def destroy(self):
        """Destroy zmq contex."""
        # context.destroy depends on pyzmq >= 2.1.10
        self.ctx.destroy(0)
