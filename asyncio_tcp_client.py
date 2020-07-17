import asyncio
from config import port_no, conn_qty
from time import time

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
        tasks.append(connect_client())
    
    await asyncio.gather(*tasks)

    
if __name__ == '__main__':
    start = time()
    asyncio.run(run_multiple_clients())
    print(f'it took {time() - start} secs')