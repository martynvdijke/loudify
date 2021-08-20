# Worker 

TODO


## CLI

There is a cli interface available that starts a loudify worker and is mainly useful for debugging purposes.

```
  -h, --help            show this help message and exit
  -p PORT, --port PORT  Specify the tcp port to bind to [default=5555]
  -a ADDRESS, --address ADDRESS
                        Specify the broker address to connect to[default='localhost']
  -s SERVICE, --service SERVICE
                        Specify the service the worker provides to[default='echo']
  -v, --verbose         set loglevel to INFO
  -vv, --very-verbose   set loglevel to DEBUG

```