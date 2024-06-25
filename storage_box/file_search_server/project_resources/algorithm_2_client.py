import socket  # Import the socket module for network communication
import ssl  # Import the SSL module for secure communication


# Define the host and port as constants
HOST: str = '127.0.0.1'
PORT: int = 1001
SSL_AUTH: bool = True
SSL_CERT: str = 'self_signed.crt'

# SSL context setup
context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)  # Create a default SSL context for server authentication
context.load_verify_locations(SSL_CERT)  # Load the certificate for SSL


def send_query(query: str) -> None:
    """
    Send a query to the server and print the response.

    Args:
        query (str): The query string to send to the server.

    Example:
        send_query("Hello, server!")
    """
    with socket.create_connection((HOST, PORT)) as sock:  # Establish a connection to the server
        if SSL_AUTH:
            sock = context.wrap_socket(sock, server_hostname=HOST)  # Wrap the socket with SSL if required
        sock.sendall(query.encode('utf-8'))  # Send the query to the server encoded in UTF-8
        response = sock.recv(1024)  # Receive the response from the server (up to 1024 bytes)
        print(f"Server response: {response.decode('utf-8')}")  # Print the server's response decoded from UTF-8


def main() -> None:
    """
    Main function to prompt the user for a query and send it to the server.

    Example:
        Enter the string to search: Hello, server!
        Server response: Hello, client!
    """
    query = input("Enter the string to search: ")  # Prompt the user to enter a query string
    send_query(query)  # Send the query to the server


if __name__ == "__main__":
    main()  # Call the main function if this script is executed directly
