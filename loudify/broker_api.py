"""Broker API."""

import logging
import time
from binascii import hexlify
import zmq

from . import zhelpers
from . import definitions
from . import broker_worker_api
from . import broker_service_api

# pylint: disable=R0902,E1101,R1705,R0912
_logger = logging.getLogger(__name__)


class Broker:
    """Broker API.

    Implements the Majordomo Protocol broker of http:#rfc.zeromq.org/spec:7
    and spec:8
    """

    # We'd normally pull these from config data
    INTERNAL_SERVICE_PREFIX = b"mmi."
    HEARTBEAT_LIVENESS = 5  # 3-5 is reasonable
    HEARTBEAT_INTERVAL = 2500  # msecs
    HEARTBEAT_EXPIRY = HEARTBEAT_INTERVAL * HEARTBEAT_LIVENESS

    # ---------------------------------------------------------------------

    ctx = None  # Our context
    socket = None  # Socket for clients & workers
    poller = None  # our Poller

    heartbeat_at = None  # When to send HEARTBEAT
    services = None  # known services
    workers = None  # known workers
    waiting = None  # idle workers

    verbose = False  # Print activity to stdout

    # ---------------------------------------------------------------------

    def __init__(self, verbose=False):
        """
        Initialize the broker state.

        @param verbose: boolean variable to turn on more verbose logging
        """

        self.verbose = verbose
        self.services = {}
        self.workers = {}
        self.waiting = []
        self.heartbeat_at = time.time() + 1e-3 * self.HEARTBEAT_INTERVAL
        self.ctx = zmq.Context()
        self.socket = self.ctx.socket(zmq.ROUTER)
        self.socket.linger = 0
        self.poller = zmq.Poller()
        self.poller.register(self.socket, zmq.POLLIN)
        self.packets_client_in = 0
        self.packets_client_out = 0
        self.packets_workers_in = 0
        self.packets_workers_out = 0
        self.packets_processed = 0

    # ---------------------------------------------------------------------

    def mediate(self):
        """Main broker work happens here."""
        while True:
            try:
                items = self.poller.poll(self.HEARTBEAT_INTERVAL)
            except KeyboardInterrupt:
                break  # Interrupted
            # if there is an request to the broker
            if items:
                msg = self.socket.recv_multipart()

                if self.verbose:
                    logging.info("I: received message:")
                    zhelpers.dump(msg)

                # get the data from the packet
                sender = msg.pop(0)
                empty = msg.pop(0)
                if empty != b"":
                    _logger.error("E: invalid empty space in message")

                header = msg.pop(0)

                if definitions.C_CLIENT == header:
                    self.process_client(sender, msg)
                elif definitions.W_WORKER == header:
                    self.process_worker(sender, msg)
                else:
                    logging.error("E: invalid message: %s", header)
                    zhelpers.dump(msg)

            self.purge_workers()
            self.send_heartbeats()

    def destroy(self):
        """Disconnect all workers, destroy context."""
        while self.workers:
            self.delete_worker(self.workers.values()[0], True)
        self.ctx.destroy(0)

    def process_client(self, sender, msg):
        """
        Process a request coming from a client.

        @param sender:
        @param msg:
        @return:
        """

        if len(msg) < 2:
            _logger.warning("E: did not receive the right msg length from the client")
        service = msg.pop(0)
        # Set reply return address to client sender
        msg = [sender, b""] + msg
        # if self.verbose:
        #     self.packets_clients_in += 1
        if service.startswith(self.INTERNAL_SERVICE_PREFIX):
            self.service_internal(service, msg)
        else:
            self.dispatch(self.require_service(service), msg)

    def process_worker(self, sender, msg):
        """
        Process message sent to us by a worker.

        @param sender:
        @param msg:
        @return:
        """

        if len(msg) < 1:
            _logger.error("E: msg length is <1, invalid msg.")
        # if self.verbose:
        #     self.packets_workers_in += 1

        command = msg.pop(0)
        # print(command)
        worker_ready = hexlify(sender) in self.workers
        worker = self.require_worker(sender)

        if definitions.W_READY == command:
            if len(msg) < 1:
                _logger.error("E: invalid service name.")

            service = msg.pop(0)
            # Not first command in session or Reserved service name
            if worker_ready or service.startswith(self.INTERNAL_SERVICE_PREFIX):
                self.delete_worker(worker, True)
            else:
                # Attach worker to service and mark as idle
                worker.service = self.require_service(service)
                self.worker_waiting(worker)

        elif definitions.W_REPLY == command:
            if worker_ready:
                # Remove & save client return envelope and insert the
                # protocol header and service name, then rewrap envelope.
                client = msg.pop(0)
                # empty = msg.pop(0)  # ?
                msg = [client, b"", definitions.C_CLIENT, worker.service.name] + msg
                self.socket.send_multipart(msg)
                self.worker_waiting(worker)
            else:
                self.delete_worker(worker, True)

        elif definitions.W_HEARTBEAT == command:
            if worker_ready:
                worker.expiry = time.time() + 1e-3 * self.HEARTBEAT_EXPIRY
            else:
                self.delete_worker(worker, True)

        elif definitions.W_DISCONNECT == command:
            self.delete_worker(worker, False)
        else:
            _logger.error("E: invalid message command: %s", command)
            zhelpers.dump(msg)

    def delete_worker(self, worker, disconnect):
        """
        Delete worker from all data structures, and deletes worker.

        @param worker:
        @param disconnect:
        @return:
        """

        if worker is None:
            _logger.error("E: Worker is None, invalid msg.")
        if disconnect:
            self.send_to_worker(worker, definitions.W_DISCONNECT, None, None)

        if worker.service is not None:
            worker.service.waiting.remove(worker)
        self.workers.pop(worker.identity)

    def require_worker(self, address):
        """
        Find the worker (creates if necessary).

        @param address:
        @return:
        """

        if address is None:
            _logger.error("E: adders is None, invalid msg.")
        identity = hexlify(address)
        worker = self.workers.get(identity)
        if worker is None:
            worker = broker_worker_api.Worker(identity, address, self.HEARTBEAT_EXPIRY)
            self.workers[identity] = worker
            if self.verbose:
                _logger.info("I: registering new worker: %s", identity)

        return worker

    def require_service(self, name):
        """
        Locate the service (creates if necessary).

        @param name:
        @return:
        """

        if name is None:
            _logger.error("E: name is None, invalid msg.")
        service = self.services.get(name)
        if service is None:
            service = broker_service_api.Service(name)
            self.services[name] = service

        return service

    def bind(self, endpoint):
        """
        Bind broker to endpoint, can call this multiple times.

        We use a single socket for both clients and workers.

        @param endpoint:
        @return:
        """

        self.socket.bind(endpoint)
        _logger.info("I: broker/0.1.1 is active at %s", endpoint)

    def service_internal(self, service, msg):
        """
        Handle internal service according to 8/MMI specification.

        @param service:
        @param msg:
        @return:
        """

        returncode = b"501"
        _logger.debug("D : Handling internal request.")
        if service == b"mmi.service":
            name = msg[-1]
            returncode = b"200" if name in self.services else b"404"
        msg[-1] = returncode

        # insert the protocol header and service name after the routing envelope ([client, ''])
        msg = msg[:2] + [definitions.C_CLIENT, service] + msg[2:]
        self.socket.send_multipart(msg)

    def send_heartbeats(self):
        """Send heartbeats to idle workers if it's time."""
        if time.time() > self.heartbeat_at:
            for worker in self.waiting:
                self.send_to_worker(worker, definitions.W_HEARTBEAT, None, None)

            self.heartbeat_at = time.time() + 1e-3 * self.HEARTBEAT_INTERVAL

    def purge_workers(self):
        """Look for & kill expired workers.

        Workers are oldest to most recent, so we stop at the first alive worker.
        """
        while self.waiting:
            worker = self.waiting[0]
            if worker.expiry < time.time():
                _logger.info("I: deleting expired worker: %s", worker.identity)
                self.delete_worker(worker, False)
                self.waiting.pop(0)
            else:
                break

    def worker_waiting(self, worker):
        """
        Worker is now waiting for work.

        @param worker:
        @return:
        """

        # Queue to broker and service waiting lists
        self.waiting.append(worker)
        worker.service.waiting.append(worker)
        worker.expiry = time.time() + 1e-3 * self.HEARTBEAT_EXPIRY
        self.dispatch(worker.service, None)

    def dispatch(self, service, msg):
        """
        Dispatch requests to waiting workers as possible.

        @param service:
        @param msg:
        @return:
        """

        if service is None:
            _logger.error("E: service is None, msg invalid.")
        # Queue message if any
        if msg is not None:
            service.requests.append(msg)
        self.purge_workers()
        while service.waiting and service.requests:
            msg = service.requests.pop(0)
            worker = service.waiting.pop(0)
            self.waiting.remove(worker)
            self.send_to_worker(worker, definitions.W_REQUEST, None, msg)

    def send_to_worker(self, worker, command, option, msg=None):
        """
        Send message to worker.

        If message is provided, sends that message.

        @param worker:
        @param command:
        @param option:
        @param msg:
        @return:
        """

        if msg is None:
            msg = []
        elif not isinstance(msg, list):
            msg = [msg]

        # Stack routing and protocol envelopes to start of message
        # and routing envelope
        if option is not None:
            msg = [option] + msg
        msg = [worker.address, b"", definitions.W_WORKER, command] + msg

        if self.verbose:
            _logger.info("I: sending %r to worker", command)
            zhelpers.dump(msg)

        self.socket.send_multipart(msg)
