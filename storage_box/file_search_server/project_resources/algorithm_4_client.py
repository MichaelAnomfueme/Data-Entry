"""
This module Sends a query to a server and receives the response from the server using a socket connection.

Example:
    $ python client.py
    Enter the string to search: hello
    Server response: connected!
"""
import socket

# Define the host and port as constants
host: str = '127.0.0.1'
port: int = 1001
psk_auth: bool = True
psk: str = '356'


def main():
    client_input = input("Enter the string to search: ")
    send_query(client_input)


# Function to send a query to the server
def send_query(client_input):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        try:
            client.connect((host, port))  # Connect to the specified host and port
            query: str = psk + client_input if psk_auth else client_input  # Construct the query string If PSK
            # authentication is enabled, prepend the PSK to the query if not send the query to the server
            client.sendall(query.encode('utf-8'))  # Send the query to the server
            response: str = client.recv(1024).decode('utf-8')  # Receive the response from the server
            print(f"Server response: {response}")  # Print the server's response
        except Exception as e:  # Handle exceptions and OS errors
            print(f"DEBUG: Connection failed server may not be online {e}")  # Log the error
            return None


if __name__ == '__main__':
    main()
