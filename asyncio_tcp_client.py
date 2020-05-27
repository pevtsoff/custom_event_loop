import asyncio
from config import port_no, conn_qty


async def connect_client():
    reader, writer = await asyncio.open_connection('localhost', port_no)
    message = "hello from client"
    print(f'sending messag: {message}')
    writer.write(message.encode())
    data = await reader.read(100)
    print(f'received message: {data}')
    writer.close
    print('Socket Closed')
    return data


async def run_multiple_clients():
    tasks = []
    
    for ind in range(conn_qty):
        tasks.append(asyncio.create_task(connect_client()))
    
    done, pending = await asyncio.wait(tasks, timeout=300)
    
    print(f'done: {done}')
    print(f'pending: {pending}')
    for d in done:
        print(f'result is {d.result()}')

    
if __name__ == '__main__':
    asyncio.run(run_multiple_clients())