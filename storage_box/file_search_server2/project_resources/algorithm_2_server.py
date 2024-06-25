from configparser import ConfigParser
import socket
import ssl
import threading
import time
from typing import Optional

# Load the configuration file config.ini
config = ConfigParser()
config.read('algorithm_2_config.ini')

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


def file_reader():
    """ Generator function to read the file line by line."""
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()


def settings_notice(context: Optional[ssl.SSLContext]) -> None:
    """Print debug messages for SSL authentication and reread on query settings

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
    """ Create a server socket and start listening for client connections."""
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
    """Handle client connections and process the string search query.

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
    """Search for a string in the file.

    Parameters:
        search_string (str): The string to search for.

    Returns:
        bool: True if the string is found, False otherwise.
    """
    if reread_on_query:
        file_lines = file_reader()
    else:
        file_lines = iter(file_contents)

    for line in file_lines:
        if line == search_string:
            return True
    return False


if __name__ == "__main__":
    file_contents = list(file_reader())
    create_server()
