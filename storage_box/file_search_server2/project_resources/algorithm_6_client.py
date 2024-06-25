import socket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

HOST = '127.0.0.1'  # Server hostname or IP address
PORT = 1001  # Server port
PSK = '356'  # Replace with your PSK


def generate_hmac(key, message):
    """Generate an HMAC (Hash-based Message Authentication Code) using the provided key and message.
    Args:
        key (bytes): The key to use for HMAC generation.
        message (bytes): The message to generate the HMAC for.
    Returns:
        bytes: The computed HMAC.
    """
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'',
        iterations=100000,
    )
    derived_key = kdf.derive(key)
    digest = hashes.Hash(hashes.SHA256())
    digest.update(derived_key)
    digest.update(message)
    hmac = digest.finalize()
    return hmac


# Connect to the server
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))

    # Prompt the user for input
    user_input = input('Enter a string to search: ')

    # Generate the HMAC for the user input using the PSK
    psk_bytes = PSK.encode()
    message = user_input.encode()
    hmac = generate_hmac(psk_bytes, message)

    # Send the HMAC and the user input to the server
    s.sendall(hmac + message)

    # Receive the response from the server
    response = s.recv(1024).decode()
    print(response)
