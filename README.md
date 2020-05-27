## Custom even loop on socket callbacks

This is a simplest implementation of a tcp echo server based on custom async 'reactor' event loop, which can handle tens of thousands connections. Each connection will be processed sequentially in one thread.
