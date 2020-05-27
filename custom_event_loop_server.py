import socket
import selectors
from config import port_no

selector = selectors.DefaultSelector()

def create_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port_no))
    server_socket.listen()
    selector.register(
        fileobj=server_socket,
        events=selectors.EVENT_READ,
        data=accept_connection
    )
    print(f'TCP Server is UP!')


def accept_connection(server_socket):
    client_socket, addr = server_socket.accept()
    print(f"Connection from: {addr}")
    selector.register(
        fileobj=client_socket,
        events=selectors.EVENT_READ,
        data=send_message
    )


def send_message(client_socket):
    request_data = client_socket.recv(4096)
    if request_data:
        print(f'received from client: {request_data}')
        response = f'Your request is: {request_data}'.encode()
        client_socket.send(response)
    else:
        selector.unregister(client_socket)
        client_socket.close()
        


def run_event_loop():
    while True:
        events = selector.select()
        
        for key, event in events:
            callback = key.data
            callback(key.fileobj)


if __name__ == '__main__':
    create_server()
    run_event_loop()