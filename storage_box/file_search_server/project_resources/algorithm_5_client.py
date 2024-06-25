"""
This module demonstrates how to send a query to a server using a socket connection.

It includes several features:
    1. Creates a socket object for a TCP connection.
    2. Connects to the specified host and port.
    3. If PSK authentication is enabled, prepends the PSK to the user's input string.
    4. Sends the query to the server.
    5. Receives the response from the server.
    6. Prints the server's response.

Example:
    $ python client.py
    Enter the string to search: hello
    Server response: Hello, world!
"""

import socket  # Import the socket module

HOST = "127.0.0.1"  # The server's hostname or IP address
PORT = 1001  # The port used by the server
PSK_AUTH = True  # Flag to enable or disable pre-shared key authentication
PSK = "35678876432468986543466887654443"  # Pre-shared key for authentication


def get_user_input() -> str:
    """
    Prompts the user to enter a string and returns the input.

    Returns:
        str: The user's input string.
    """
    user_input = input("Enter the string to search: ")  # Prompt the user for input
    return user_input  # Return the user's input


def send_query(query: str) -> str:
    """
    Sends a query to the server and returns the server's response.

    Args:
        query (str): The query string to send to the server.

    Returns:
        str: The server's response to the query.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:  # Create a socket object
        client.connect((HOST, PORT))  # Connect to the server
        if PSK_AUTH:  # If PSK authentication is enabled
            query = PSK + query  # Prepend the PSK to the query
        client.sendall(query.encode("utf-8"))  # Send the query to the server
        response = client.recv(1024).decode("utf-8")  # Receive the server's response
    return response  # Return the server's response


def main() -> None:
    """
    The main function of the program.

    This function prompts the user for input, sends the query to the server,
    and prints the server's response.
    """
    user_input = get_user_input()  # Get the user's input
    server_response = send_query(user_input)  # Send the query to the server
    print(f"Server response: {server_response}")  # Print the server's response


if __name__ == "__main__":
    main()  # Call the main function if the script is run directly
