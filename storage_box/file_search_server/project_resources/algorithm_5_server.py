import asyncio
import re
import time
from configparser import ConfigParser
import aiofiles
from typing import Optional

# Create a ConfigParser object
config = ConfigParser()
config.read('algorithm_5_config.ini')

# Get configuration values
file_path: str = config.get('file_path', 'linuxpath')
host: str = config.get('server', 'host')
port: int = config.getint('server', 'port')
psk_auth: bool = config.getboolean('security_setting', 'psk_auth')
psk: str = config.get('security_setting', 'psk')
reread_on_query: bool = config.getboolean('query_setting', 'reread_on_query')

# Initialize file contents to None so the file is read once if reread_on_query is False
file_contents: Optional[str] = None

def log_settings() -> None:
    """
    Log the server settings to the console.
    for PSK authentication and reread on query status.

    """
    if psk_auth:
        print("DEBUG: PSK authentication enabled")
    else:
        print("DEBUG: PSK authentication disabled")

    if reread_on_query:
        print("DEBUG: Reread on query enabled")
    else:
        print("DEBUG: Reread on query disabled")

async def read_file_once() -> str:
    """
    Read the file and store its contents in memory.

    Returns:
        str: The contents of the file.
    """
    global file_contents
    if file_contents is None:
        async with aiofiles.open(file_path, 'r') as file:
            file_contents = await file.read()
    return file_contents

async def handle_client(reader: asyncio.StreamReader, writer: asyncio.StreamWriter) -> None:
    """
    Handle the client connection and process the request.

    Args:
        reader (asyncio.StreamReader): Async reader for the client socket.
        writer (asyncio.StreamWriter): Async writer for the client socket.

    """
    addr = writer.get_extra_info('peername')
    try:
        print(f"DEBUG: Connection from {addr} has been established.")
        start_time = time.time()
        data = await reader.read(1024)
        data = data.decode('utf-8').rstrip('\x00').strip()

        if psk_auth:
            if not data.startswith(psk):
                writer.write(b'Authentication failed - PSK mismatch.')
                await writer.drain()
                raise ValueError('DEBUG: PSK Authentication failed.')
            data = data[len(psk):]

        print(f"DEBUG: Query received from {addr}: {data}")

        if reread_on_query:
            async with aiofiles.open(file_path, 'r') as file:
                contents = await file.read()
        else:
            contents = await read_file_once()

        match = re.search(f'^{re.escape(data)}$', contents, re.MULTILINE)
        response = 'STRING EXISTS\n' if match else 'STRING NOT FOUND\n'

        writer.write(response.encode('utf-8'))
        await writer.drain()

        execution_time = time.time() - start_time
        print(f"DEBUG: Response sent to {addr}: {response.strip()}")
        print(f"DEBUG: Execution time: {execution_time:.5f}s")

    except Exception as e:
        writer.write(b'Could not handle your request pls try again later')
        await writer.drain()
        print(f"DEBUG: Error handling client {addr}: {e}")

    finally:
        writer.close()
        await writer.wait_closed()

async def start_server() -> None:
    """
    Start the server and listen for incoming connections.

    """
    server = await asyncio.start_server(handle_client, host, port)

    async with server:
        print(f"DEBUG: Server listening on Host: {host} Port: {port}")
        log_settings()
        await server.serve_forever()

if __name__ == '__main__':
    asyncio.run(start_server())
