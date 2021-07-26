# Broker

The broker forms the central hart of the architecture and is responsible for a number of part:

- Forwarding request to the workers
- Keeping the connection alive between broker and worker by
  - Registration of new workers
  - Deleting old (expired) workers
- Routing the requests (including internal requests)

## CLI

To start the broker run `loudify-broker -p $port` where  `$port` is a sn available and forwarded TCP port.

```
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specify the txp port to bind to [default=5555]
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
```