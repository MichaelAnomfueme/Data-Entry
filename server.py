"""This module provides a server that listens for
string search queries from clients.
When a client sends a query, the server searches for
the string in a file and responds with "STRING EXISTS" or
"STRING NOT FOUND" accordingly.

The server can be configured to use PSK authentication
and to reread the file for each query or only once at startup.

Example usage:
    1. Configure the server settings in the 'config.ini' file.
    2. Run the module: 'python server.py'

The server will listen on the configured host and port,
and log debug messages to the console.
"""

import sys
import time
import socket
import hashlib
import threading
from configparser import ConfigParser

# Create a ConfigParser object and read the configuration file
config = ConfigParser()
config.read("config.ini")

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
PSK_HASH: str = hashlib.sha256(PSK.encode()).hexdigest()

# Set constant to preload file contents
FILE_CONTENTS_SET: set[str] | None = None


def log_settings() -> None:
    """Check and close server if directory is empty.

    Log server settings to the console.
    Load and store file content in memory.
    """
    if PSK_AUTH and not PSK:
        print("DEBUG: PSK authentication is enabled, "
              "but the PSK is empty. Stopping the server.")
        sys.exit(1)
    if not FILE_PATH:
        print("DEBUG: File path is empty. Stopping the server.")
        sys.exit(1)

    # Log server start
    print(f"DEBUG: Server listening on Host: {HOST} Port: {PORT}")
    # Log PSK authentication status
    print(f"DEBUG: PSK authentication {'enabled' if PSK_AUTH else 'disabled'}")
    # Log reread on query status
    print(f"DEBUG: Reread on query {
        'enabled' if REREAD_ON_QUERY else 'disabled'
    }")


def load_file_contents() -> None:
    """Load file contents into memory."""
    global FILE_CONTENTS_SET
    if FILE_CONTENTS_SET is None:
        try:
            # Load file contents into memory if not already loaded
            with open(FILE_PATH, "r", encoding="utf-8") as file:
                file_contents: str = file.read()
            FILE_CONTENTS_SET = set(file_contents.splitlines())
        except FileNotFoundError as error:
            print(f"DEBUG: {FILE_PATH} file not found: {error}\nStopping the server.")
            sys.exit(1)
        except Exception as error:
            print(f"DEBUG: Error loading file: {error}\nStopping the server.")
            sys.exit(1)


def start_server() -> None:
    """Start the server and listen for incoming connections."""
    try:
        # Create a TCP/IP socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Bind the socket to the host and port
        server.bind((HOST, PORT))
        # Listen for incoming connections
        server.listen(5)
        # Call function to load file contents into memory
        load_file_contents()
        # Log current PSK authentication and reread on query status
        log_settings()

        while True:
            # Continuously accept connections
            conn: socket.socket
            addr: tuple[str, int]
            conn, addr = server.accept()
            # Create a new thread for the connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            # Start the new thread
            thread.start()
    except socket.error as error:
        print(f"DEBUG: Socket error: {error}")
        sys.exit(1)
    except Exception as error:
        print(f"DEBUG: Error handling connection: {error}")
        sys.exit(1)


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """Handle the client connection and process the request.

    Args:
        conn (socket.socket): The client socket connection.
        addr (tuple[str, int]): The client address (host, port).
    """
    try:
        # Log the established connection
        print(f"DEBUG: Connection from {addr} has been established.")
        # Timeout if process takes more than necessary
        conn.settimeout(0.05)
        # Receive and decode data from the client
        data: str = conn.recv(1024).decode(
            "utf-8", errors="replace").rstrip("\x00")
        # Record the start time
        start_time: float = time.time()

        if PSK_AUTH:
            if not data.startswith(PSK_HASH):
                # Send authentication failure message
                conn.sendall(b"Authentication failed - PSK mismatch.")
                # Log the authentication error
                print("DEBUG: PSK Authentication failed.")
                return

            # Remove psk_hash from the received data
            data = data[len(PSK_HASH):]

        if not PSK_AUTH:
            if data.startswith(PSK_HASH):
                # Remove psk_hash from the received data
                # when psk_auth is false and client psk_auth is true.
                data = data[len(PSK_HASH):]

        # Log the received query
        print(f"DEBUG: Query received from {addr}: {data}")

        if REREAD_ON_QUERY:
            # Open the file for reading
            with open(FILE_PATH, "r", encoding="utf-8") as text:
                # Read the file contents and split into lines
                match: list[str] = text.read().splitlines()
            # Check if the query matches any line in the file
            response: str = (
                "STRING EXISTS\n" if data in match else "STRING NOT FOUND\n"
            )
        else:
            # Check if the query matches any line in the preloaded set
            response = 'STRING EXISTS\n' if data in FILE_CONTENTS_SET else 'STRING NOT FOUND\n'

        # Send the response to the client
        conn.sendall(response.encode("utf-8"))
        # Calculate the execution time
        execution_time: float = time.time() - start_time
        # Log response sent to client
        print(f"DEBUG: Response sent to {addr}: {response.strip()}.")
        # Log time taken to execute
        print(f"DEBUG: Execution time: {execution_time:.10f}s")
    except socket.timeout as error:
        # Send feedback to client
        conn.sendall(b"Could not handle your request. Please try again later.")
        # Log the error
        print(f"DEBUG: Connection from {addr} timed out: {error}.")
    except Exception as error:
        # Send feedback to client
        conn.sendall(b"Could not handle your request. Please try again later.")
        # Log the error
        print(f"DEBUG: Error handling client {addr}: {error}.")
    finally:
        # Close the client connection
        conn.close()


if __name__ == "__main__":
    start_server()
