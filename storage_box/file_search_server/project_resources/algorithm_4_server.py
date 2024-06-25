import socket
import threading
import re
import time
from configparser import ConfigParser

config = ConfigParser()  # Create a ConfigParser object

config.read('algorithm_4_config.ini')  # Read the configuration file

file_path: str = config.get('file_path', 'linuxpath')  # Get file path from the config

host: str = config.get('server', 'host')  # Get server host from the config
# (The hostname or IP address to bind the server to.)

port: int = config.getint('server', 'port')  # Get server port from the config (The port number to listen on.)

psk_auth: bool = config.getboolean('security_setting', 'psk_auth')  # Get PSK auth setting

psk: str = config.get('security_setting', 'psk')  # Get PSK value from the config

reread_on_query: bool = config.getboolean('query_setting', 'reread_on_query')  # Get reread on query setting

file_contents = None  # Initialize file contents to None so the file is read once if REREAD_ON_QUERY is False


def log_settings() -> None:
    """
    Log the server settings to the console.
    for PSK authentication and reread on query status
    """
    if psk_auth:  # Check if PSK authentication is enabled
        print("DEBUG: PSK authentication enabled")  # Log that PSK authentication is enabled
    else:  # If PSK authentication is disabled
        print("DEBUG: PSK authentication disabled")  # Log that PSK authentication is disabled

    if reread_on_query:  # Check if reread on query is enabled
        print("DEBUG: Reread on query enabled")  # Log that reread on query is enabled
    else:  # If reread on query is disabled
        print("DEBUG: Reread on query disabled")  # Log that reread on query is disabled


# Function to start the server
def start_server() -> None:
    """
    Start the server and listen for incoming connections.
    """
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a TCP/IP socket
        server.bind((host, port))  # Bind the socket to the host and port
        server.listen(5)  # listen to incoming connection
        print(f"DEBUG: Server listening on Host: {host} Port: {port}")  # Log server start
        log_settings()  # Call the function to log current PSK authentication and reread on query status

        while True:  # Continuously accept connections
            conn, addr = server.accept()  # Accept a new connection
            thread = threading.Thread(target=handle_client, args=(conn, addr))  # Create a new thread for the connection
            thread.start()  # Start the new thread

    except (Exception, OSError) as e:  # Handle exceptions and OS errors
        print(f"DEBUG: Error handling connection: {e}")  # Log the error


def read_file_once() -> str:
    """
    Read the file and store its contents in memory.
    Returns:
        str: The contents of the file.
    """
    global file_contents  # Use global variable to store file contents
    if file_contents is None:  # Check if file contents are not already loaded
        with open(file_path, 'r') as file:  # Open the file for reading
            file_contents = file.read()  # Read the file contents
    return file_contents  # Return the file contents


def handle_client(conn, addr) -> None:
    """
    Handle the client connection and process the request.
    Args:
        conn (socket.socket): The client socket connection.
        addr (tuple[str, int]): The client address (host, port).
    """
    try:
        print(f"DEBUG: Connection from {addr} has been established.")  # Log the established connection
        start_time = time.time()  # Record the start time

        conn.settimeout(0.05)
        data = conn.recv(1024).decode('utf-8').rstrip('\x00').strip()  # Receive and decode data from the client
        if psk_auth:  # Check if PSK authentication is enabled
            if not data.startswith(psk):  # Check if the data received starts with the PSK
                conn.sendall(b'Authentication failed - PSK mismatch.')  # Send authentication failure message to client
                print('DEBUG: PSK Authentication failed.')  # Raise an authentication error
                return None

            data = data[len(psk):]  # Remove PSK from the received data

        if not psk_auth:
            if data.startswith(psk):
                data = data[len(psk):]  # Remove PSK from the received data

        print(f"DEBUG: Query received from {addr}: {data}")  # Log the received query

        if reread_on_query:  # Check if reread on query is enabled
            with open(file_path, 'r') as file:  # Open the file for reading
                contents = file.read()  # Read the file contents
        else:  # If reread on query is disabled
            contents = read_file_once()  # call the function read_file_once()
            # and use the previously loaded file contents

        match = re.search(f'^{re.escape(data)}$', contents, re.MULTILINE)  # search for a full match of the received string in the file
        response = 'STRING EXISTS\n' if match else 'STRING NOT FOUND\n'  # Create a response dialog based on the match

        conn.sendall(response.encode('utf-8'))  # Send the response to the client
        execution_time = time.time() - start_time  # calculate the execution time
        print(f"DEBUG: Response sent to {addr}: {response.strip()}")  # Log response sent to client
        print(f"DEBUG: Execution time: {execution_time:.5f}s")  # Log time taken to execute

    except Exception as e:  # Handle exceptions
        conn.sendall(b'Could not handle your request pls try again later')  # Send feedback to client
        print(f"DEBUG: Error handling client {addr}: {e}")  # log the error

    finally:
        conn.close()  # Close the client connection


# Run the server
if __name__ == '__main__':
    start_server()
