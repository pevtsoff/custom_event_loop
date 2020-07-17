import socket, time
from select import select
from config import port_no
from collections import deque


tasks = deque()
recv_wait = {}
send_wait = {}


def create_server():
    server_socket = socket.socket()
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', port_no))
    server_socket.listen()
    print(f'TCP Server is UP!')
    
    return server_socket
    

def serve(server_socket):

    while True:
        yield 'recv', server_socket

        client_sock, addr = server_socket.accept()
        print(f'connection from {addr}')
        tasks.append(communicate_with_client(client_sock))

        
        
def communicate_with_client(client_socket):
    while True:
        
        yield 'recv', client_socket
        msg = client_socket.recv(4096)

        if not msg:
            break
        else:
            print(f'received from client: {msg}')
            response = f'you sent: {msg}'.encode()
        
            yield 'send', client_socket
            client_socket.send(response)
    
    print(f'closing socket {client_socket.fileno()}')
    client_socket.close()


def get_tasks():
    while not tasks:
        can_recv, can_send, _ = select(recv_wait, send_wait, [])
        
        for sock in can_recv:
            tasks.append(recv_wait.pop(sock))
        for sock in can_send:
            tasks.append(send_wait.pop(sock))


def event_loop():
    while any([tasks, recv_wait, send_wait]):
        try:
            get_tasks()
           
            task = tasks.popleft()
            reason, sock = task.__next__()
            
            if reason == 'recv':
                recv_wait[sock] = task
            if reason == 'send':
                send_wait[sock] = task
                
        except StopIteration:
            print(f'done all {reason} tasks!')


if __name__ == '__main__':
    server_socket = create_server()
    tasks.append(serve(server_socket))
    event_loop()