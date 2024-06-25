"""
This module Sends a query to a server and receives the response from the server using a socket connection.

Example:
    $ python client.py
    Enter the string to search: hello
    Server response: connected!
"""
import hashlib
import socket

# Define the host and port as constants
host: str = '127.0.0.1'  # Replace with your host
port: int = 1001  # Replace with your private port number
psk_auth: bool = True  # Replace with False if you want to turn off
psk: str = '70'  # Replace with your private PSK
psk_hash = hashlib.sha256(psk.encode()).hexdigest()


def get_user_input() -> str:
    """
    Prompts the user to enter a string to search.

    Returns:
        str: The user's input string.
    """
    return input("Enter the string to search: ")


def main() -> None:
    """
    Establishes a connection to the server, sends a query, and prints the server's response.

    This function performs the following steps:
    1. Creates a socket object for a TCP connection.
    2. Connects to the specified host and port.
    3. If PSK authentication is enabled, prepends the PSK to the user's input string.
    4. Sends the query to the server.
    5. Receives the response from the server.
    6. Prints the server's response.
    """

    client_input: str = get_user_input()  # Get the user's input string
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:  # Ensure the socket is closed after use
        # Connect to the server
        try:
            client.connect((host, port))  # Connect to the specified host and port
            query: str = psk_hash + client_input if psk_auth else client_input  # Construct the query string If PSK
            # authentication is enabled, prepend the PSK to the query if not send the query to the server
            client.sendall(query.encode('utf-8'))  # Send the query to the server
            response: str = client.recv(1024).decode('utf-8')  # Receive the response from the server
            print(f"Server response: {response}")  # Print the server's response
        except Exception as e:  # Handle exceptions and OS errors
            print(f"DEBUG: Connection failed server may not be online {e}")  # Log the error
            return None


if __name__ == "__main__":
    main()
