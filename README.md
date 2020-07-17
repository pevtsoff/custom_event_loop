## Custom even loop on socket callbacks

#### selectors_event_loop_server
This is a simplest implementation of a tcp echo server based on selectors module and 'reactor' pattern event loop, which can handle tens of thousands connections. Each connection will be processed sequentially in the same thread as eventloop itself

#### gen_based_event_loop_server.py
Generator based event loop with  round-robin logic. Is slower than selectors event loop server.