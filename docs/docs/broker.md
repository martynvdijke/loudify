# Broker

The broker forms the central hart of the architecture and is responsible for a number of part:

- Forwarding request to the workers
- Keeping the connection alive between broker and worker by
  - Registration of new workers
  - Deleting old (expired) workers
- Routing the requests (including internal requests)
