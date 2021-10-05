"""Broker definitions."""
#  This is the version of MDP/Client we implement
C_CLIENT = b"C01"

#  This is the version of MDP/Worker we implement
W_WORKER = b"W01"

#  MDP/Server commands, as strings
W_READY = b"\001"
W_REQUEST = b"\002"
W_REPLY = b"\003"
W_HEARTBEAT = b"\004"
W_DISCONNECT = b"\005"
W_ERROR = b"\006"

commands = [None, b"READY", b"REQUEST", b"REPLY", b"HEARTBEAT", b"DISCONNECT"]

internal_commands = [b"GET_WORKERS"]
TIMEOUT = 5


# Note, Python3 type "bytes" are essentially what Python2 "str" were,
# but now we have to explicitly mark them as such.  Type "bytes" are
# what PyZMQ expects by default.  Any user code that uses this and
# related modules may need to be updated.  Here are some guidelines:
#
# String literals that make their way into messages or used as socket
# identfiers need to become bytes:
#
#   'foo' -> b'foo'
#
# Multippart messages, originally formed as lists of strings (smsg)
# need to be washed into strings of bytes (bmsg) like:
#
#   bmsg = [one.encode('utf-8') for one in smsg]
#
# A multipart message recived can be reversed
#
#   smsg = [one.decode() for one in bmsg]
