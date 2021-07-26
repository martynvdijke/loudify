# Client

Although, the client has a cli interface this is mainly useful for debugging the overall system.
The main purpose of this project is to embed the client directly into a GNU Radio flowgraph. The client packages a packet into a network packet and sends that network packet to the cloud and waits for a reply.

## Async vs Sync

This project supports both async and synchronous client modes. If you first start out running the synchronous mode is the most practical, since it will result in overall fewer errors and more clear network problems.
## CLI

There is a cli interface available that starts a loudify client and is mainly useful for debugging purposes.

```
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specify the tcp port to bind to [default=5555]
  -a ADDRESS, --address ADDRESS
                        Specify the broker address to connect to d[default='localhost']
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG
```