""" This module Sends a query to a server and receives
the response from the server using a socket connection.

Example:
    $ python client.py
    Enter the string to search: hello
    Server response: connected!
"""

import socket
import sys
import hashlib

HOST: str = '127.0.0.1'  # Replace with your host
PORT: int = 1001  # Replace with your private port number
PSK_AUTH: bool = True  # Replace with False if you want to turn off
PSK: str = '000'  # Replace with your private PSK
PSK_HASH: str = hashlib.sha256(PSK.encode()).hexdigest()


def get_user_input() -> str:
    """
    Prompts the user to enter a string to search.

    Returns:
        str: The user's input string.
    """
    return input("Enter the string to search: ")


def main() -> None:
    """
    Establishes a connection to the server, sends a query, and prints the
    server's response.

    This function performs the following steps:
    1. Creates a socket object for a TCP connection.
    2. Connects to the specified host and port.
    3. If PSK authentication is enabled, prepends the
       PSK HASH to the user's input string.
    4. Sends the query to the server.
    5. Receives the response from the server.
    6. logs the server's response.
    """

    # Get the user's input string
    client_input = get_user_input()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((HOST, PORT))
            query = f"{PSK_HASH}{client_input}" if PSK_AUTH else client_input
            client.sendall(query.encode('utf-8'))
            response = client.recv(1024).decode('utf-8')
            # Log server's response
            print(f"Server response: {response}")

        except socket.error as error:
            # Log error
            print(f"DEBUG: Socket error: {error}")
            sys.exit(1)
        except Exception as e:
            # Log error
            print(f"DEBUG: Error handling connection {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
