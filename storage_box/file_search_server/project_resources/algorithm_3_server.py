"""
This module provides a server that listens for string search queries from clients.
When a client sends a query, the server searches for the string in a file and responds
with "STRING EXISTS" or "STRING NOT FOUND" accordingly. The server can be configured
to use SSL authentication and to reread the file for each query or only once at startup.

Example usage:
    1. Configure the server settings in the 'config.ini' file.
    2. Run the module: 'python server.py'

The server will listen on the configured host and port, and print debug messages
to the console.

Configuration file format (config.ini):
    The server settings are read from the config.ini file in the same
    directory. The following settings format are available:

    [file_path]
    linuxpath = /path/to/file.txt  # Path to the file to search

    [server]
    host = 0.0.0.0  # Server IP address
    port = 8000  # Server port number

    [security_setting]
    ssl_auth = True  # Enable/disable PSK authentication
    ssl_cert_file = /path/to/cert  # SSL certificate for authentication
    ssl_key_file = /path/to/key  # SSL key for authentication

    [query_setting]
    reread_on_query = False

    Note:
    The server assumes that the file exists and is readable. If the file
    is missing or unreadable, the server will log an error and continue
    running, but client requests will fail until the file becomes available.
"""

from configparser import ConfigParser
import socket
import ssl
import threading
import time
from typing import Optional

# Load the configuration file config.ini
config = ConfigParser()
config.read('algorithm_3_config.ini')

# Load File Path
file_path: str = config.get('file_path', 'linuxpath')

# Load Server Address
host: str = config.get('server', 'host')  # The hostname or IP address to bind the server to.
port: int = config.getint('server', 'port')  # The port number to listen on.

# Load Security Settings
ssl_auth: bool = config.getboolean('security_setting', 'ssl_auth')
ssl_cert = config.get('security_setting', 'ssl_cert_file')
ssl_key = config.get('security_setting', 'ssl_key_file')


# Load Reread on Query Settings
reread_on_query: bool = config.getboolean('query_setting', 'reread_on_query')

# Read the file once if REREAD_ON_QUERY is False
file_contents = None


def settings_notice(context: Optional[ssl.SSLContext]) -> None:
    """
    Print debug messages for SSL authentication and reread on query settings

    Parameters:
        context (Optional[ssl.SSLContext]): The SSL context, if SSL authentication is enabled.
    """
    if context:
        print("DEBUG: SSL authentication enabled")
    elif not context:
        print("DEBUG: SSL authentication disabled")
    if reread_on_query:
        print("DEBUG: Reread on query enabled")
    elif not reread_on_query:
        print("DEBUG: Reread on query disabled")


def create_server() -> None:
    """
    Create a server socket and start listening for client connections.

    """
    context: Optional[ssl.SSLContext] = None
    if ssl_auth:
        try:
            context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            context.load_cert_chain(certfile=ssl_cert, keyfile=ssl_key)
        except Exception as e:
            print(f"DEBUG: Error loading ssl certificate. {e}")
            return None
    try:
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((host, port))
        server_socket.listen()
    except Exception as e:
        print(f"DEBUG: Error creating socket connection: {e}")
        return None

    print(f"DEBUG: Server listening on {host}:{port}")
    settings_notice(context)

    while True:
        conn, addr = server_socket.accept()
        if context:
            try:
                # Wrap the connection in an SSL context or timeout if process takes more than necessary
                conn.settimeout(0.05)
                conn = context.wrap_socket(conn, server_side=True)
            except Exception as e:
                print(f"DEBUG: SSL authentication with client {addr} failed: {e}")
                conn.close()
                continue

        # Start a new thread to handle the client connection
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()


def handle_client(conn: socket.socket, addr: tuple) -> None:
    """
        Handle client connections and process the string search query.

        Parameters:
            conn (socket.socket): The Client socket connection.
            addr (tuple[str, int]): The address of the client.
        """
    print(f"DEBUG: Connection from {addr} has been established.")
    try:
        start_time = time.time()
        data = conn.recv(1024).decode().rstrip('\x00')  # Receive data and strip null characters
        print(f"DEBUG: Query received from {addr}: {data}")

        search_string = data.strip()
        match = search_file(search_string)

        response = 'STRING EXISTS\n' if match else 'STRING NOT FOUND\n'
        conn.sendall(response.encode())
        execution_time = time.time() - start_time

        print(f"DEBUG: Response sent to {addr}: {response.strip()}")
        print(f"DEBUG: Execution time: {execution_time:.5f}s")
    except Exception as e:
        conn.sendall(b'Could not handle your request pls try again later')
        print(f"DEBUG: Error handling connection from {addr}: {e}")
    finally:
        conn.close()


def search_file(search_string: str) -> bool:
    """
        Search for a string in the file.
    Parameters:
        search_string (str): The string to search for.

     Returns:
        bool: True if the string is found, False otherwise.
    """
    global file_contents
    if reread_on_query or file_contents is None:
        with open(file_path, 'r') as f:
            file_contents = f.readlines()

    for line in file_contents:
        if line.strip() == search_string:
            return True
    return False


if __name__ == "__main__":
    create_server()
