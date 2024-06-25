"""This module provides a server that listens for string search queries from clients.
When a client sends a query, the server searches for the string in a file and responds
with "STRING EXISTS" or "STRING NOT FOUND" accordingly. The server can be configured
to use PSK authentication and to reread the file for each query or only once at startup.

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
    psk_auth = True  # Enable/disable PSK authentication
    psk = 1Aa@  # Pre-shared key for authentication

    [query_setting]
    reread_on_query = False  # Read file for each request or keep in memory
"""

import hashlib
import socket
import threading
import time
from configparser import ConfigParser

"""Global variables"""

# Create a ConfigParser object and read the configuration file
config = ConfigParser()
config.read('config.ini')

# Get file path, server host, and port from the config
FILE_PATH: str = config.get('FILE_PATH', 'LINUXPATH')
HOST: str = config.get('SERVER', 'HOST')
PORT: int = config.getint('SERVER', 'PORT')

# Get PSK authentication settings and the PSK value from the config
PSK_AUTH: bool = config.getboolean('SECURITY_SETTING', 'PSK_AUTH')
PSK: str = config.get('SECURITY_SETTING', 'PSK')

# Get reread on query setting from the config
REREAD_ON_QUERY: bool = config.getboolean('QUERY_SETTING', 'REREAD_ON_QUERY')

# Hash the PSK
PSK_HASH = hashlib.sha256(PSK.encode()).hexdigest()

# Preload file contents into memory
file_contents_set = None


def log_settings() -> None:
    """Check and close server if directory is empty.
    Log server settings to the console.
    load and store file content in memory.
    """
    global file_contents_set
    if PSK_AUTH and not PSK:
        print("DEBUG: PSK authentication is enabled, but the PSK is empty. Stopping the server.")
        exit(1)
    if not FILE_PATH:
        print("DEBUG: File path is empty. Stopping the server.")
        exit(1)

    # Log server start
    print("DEBUG: Server listening on Host: {} Port: {}".format(HOST, PORT))
    # Log PSK authentication status
    print("DEBUG: PSK authentication {}".format('enabled' if PSK_AUTH else 'disabled'))
    # Log reread on query status
    print("DEBUG: Reread on query {}".format('enabled' if REREAD_ON_QUERY else 'disabled'))

    if file_contents_set is None:
        try:
            # Load file contents into memory if not already loaded
            with open(FILE_PATH, 'r') as file:
                file_contents = file.read()
            file_contents_set = set(file_contents.splitlines())
        except Exception as e:
            # Log any errors encountered while loading the file
            print("DEBUG: Error loading file: {}".format(e))


def start_server() -> None:
    """Start the server and listen for incoming connections."""
    try:
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the host and port
        server.bind((HOST, PORT))
        # Listen for incoming connections
        server.listen(5)
        # Log current PSK authentication and reread on query status
        log_settings()

        while True:
            # Continuously accept connections
            conn, addr = server.accept()
            # Create a new thread for the connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            # Start the new thread
            thread.start()
    except Exception as e:
        print("DEBUG: Error handling connection: {}".format(e))


def handle_client(conn,
                  addr) -> None:
    """Handle the client connection and process the request.

    Args:
        conn (socket.socket): The client socket connection.
        addr (tuple[str, int]): The client address (host, port).
    """
    try:
        # Log the established connection
        print("DEBUG: Connection from {} has been established.".format(addr))
        # Timeout if process takes more than necessary
        conn.settimeout(0.05)
        # Receive and decode data from the client
        data = conn.recv(1024).decode('utf-8', errors='replace').rstrip('\x00').strip()
        # Record the start time
        start_time = time.time()

        if PSK_AUTH:
            if not data.startswith(PSK_HASH):
                # Send authentication failure message
                conn.sendall(b'Authentication failed - PSK mismatch.')
                # Log the authentication error
                print('DEBUG: PSK Authentication failed.')
                return

            # Remove psk_hash from the received data
            data = data[len(PSK_HASH):]

        if not PSK_AUTH:
            if data.startswith(PSK_HASH):
                # Remove psk_hash from the received data
                # when psk_auth is false and client psk_auth is true.
                data = data[len(PSK_HASH):]

        # Log the received query
        print("DEBUG: Query received from {}: {}".format(addr, data))

        if REREAD_ON_QUERY:
            # Open the file for reading
            with open(FILE_PATH, 'r') as text:
                # Read the file contents and split into lines
                match = text.read().splitlines()
            # Check if the query matches any line in the file
            response = 'STRING EXISTS\n' if data in match else 'STRING NOT FOUND\n'
        else:
            # Check if the data exists in the preloaded set
            response = 'STRING EXISTS\n' if data in file_contents_set else 'STRING NOT FOUND\n'

        # Send the response to the client
        conn.sendall(response.encode('utf-8'))
        # Calculate the execution time
        execution_time = time.time() - start_time
        # Log response sent to client
        print("DEBUG: Response sent to {}: {}".format(addr, response.strip()))
        # Log time taken to execute
        print("DEBUG: Execution time: {:.10f}s".format(execution_time))
    except Exception as e:
        # Send error feedback to client
        conn.sendall(b'Could not handle your request pls try again later')
        # Log the error
        print("DEBUG: Error handling client {}: {}".format(addr, e))
    finally:
        # Close the client connection
        conn.close()


if __name__ == '__main__':
    start_server()
