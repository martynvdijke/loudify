# encoding: utf-8
"""Helper module for example applications. Mimics ZeroMQ Guide's zhelpers.h."""
from __future__ import print_function
import binascii
from random import randint
import zmq


# pylint: disable=R0902,E1101,R1705


def socket_set_hwm(socket, hwm=-1):
    """Libzmq 2/3/4 compatible sethwm."""
    try:
        socket.sndhwm = socket.rcvhwm = hwm
    except AttributeError:
        socket.hwm = hwm


def dump(msg_or_socket):
    """Receive all message parts from socket, printing each frame neatly."""
    if isinstance(msg_or_socket, zmq.Socket):
        # it's a socket, call on current message
        msg = msg_or_socket.recv_multipart()
    else:
        msg = msg_or_socket
    print("----------------------------------------")
    for part in msg:

        if len(part) > 1000:
            print("[%03d]" % len(part))
            continue
        print("[%03d]" % len(part), end=" ")
        try:
            print(part.decode("ascii"))
        except UnicodeDecodeError:
            print(r"0x%s" % (binascii.hexlify(part).decode("ascii")))


def set_id(zsocket):
    """Set simple random printable identity on socket."""
    identity = u"%04x-%04x" % (randint(0, 0x10000), randint(0, 0x10000))
    zsocket.setsockopt_string(zmq.IDENTITY, identity)
