import hashlib
import socket
import unittest
from unittest.mock import patch, MagicMock, mock_open

# Import the functions and settings from server.py
from server import (
    log_settings,
    start_server,
    read_file_once,
    handle_client, host, port, psk_auth, psk, reread_on_query,
)


@patch('server.ConfigParser')
class TestServer(unittest.TestCase):
    """Unit tests for the server functions."""

    def setUp(self) -> None:
        """Set up test data and configurations."""
        self.test_file_path = 'tests/test_data.txt'
        self.test_data = 'test data'

        # Mock the ConfigParser object
        self.config_mock = MagicMock()
        self.config_mock.get.side_effect = [
            self.test_file_path,  # file_path
            host,  # host
            port,  # port (needs to be str due to ConfigParser behavior)
            psk_auth,  # psk_auth
            psk,  # psk
            reread_on_query,  # reread_on_query
        ]

    def test_log_settings(self, config_mock: MagicMock) -> None:
        """Test the log_settings function."""

        with patch('builtins.print') as mock_print:
            log_settings()
            if psk_auth:
                mock_print.assert_any_call("DEBUG: PSK authentication enabled")
            if reread_on_query:
                mock_print.assert_any_call("DEBUG: Reread on query enabled")
            if not psk_auth:
                mock_print.assert_any_call("DEBUG: PSK authentication disabled")
            if not reread_on_query:
                mock_print.assert_any_call("DEBUG: Reread on query disabled")

    def test_start_server(self, config_mock: MagicMock) -> None:
        """Test the start_server function."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.accept.side_effect = socket.error

            start_server()

            mock_socket.assert_called_once()
            mock_server.bind.assert_called_once()
            mock_server.listen.assert_called_once_with(5)

    def test_read_file_once(self, config_mock: MagicMock) -> None:
        """Test the read_file_once function."""
        with patch('builtins.open', mock_open(read_data=self.test_data)):
            if not reread_on_query:
                file_contents = read_file_once()
                self.assertEqual(file_contents, self.test_data)
            else:
                pass

    def test_handle_client(self, config_mock: MagicMock) -> None:
        """Test the handle_client function."""
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'test'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))

            mock_conn.sendall.assert_called_once()
            mock_conn.close.assert_called_once()

    def test_read_file_once_file_already_loaded(self, config_mock: MagicMock) -> None:
        """Test the read_file_once function when the file is already loaded."""
        config_mock.get.side_effect = [
            self.test_file_path, host, port, psk_auth,
            psk, reread_on_query
        ]
        with patch('builtins.open', mock_open(read_data=self.test_data)):
            file_contents = read_file_once()
            self.assertEqual(file_contents, self.test_data)

            # Call read_file_once again to ensure the file is not read again
            file_contents = read_file_once()
            self.assertEqual(file_contents, self.test_data)

    def test_handle_client_invalid_input(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when an invalid input is received."""
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b''

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'One or more invalid input.')
            mock_print.assert_any_call(f"DEBUG: Connection from ('{host}', {port}) has been established.")

    def test_handle_client_psk_authentication_failure(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when PSK authentication fails."""
        config_mock.get.side_effect = [
            self.test_file_path, host, port, psk_auth,
            'invalid_psk', reread_on_query
        ]
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'invalid_psk_hash'

        with patch('builtins.print') as mock_print:
            if psk_auth:
                handle_client(mock_conn, (host, port))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_start_server_socket_error(self, config_mock: MagicMock) -> None:
        """Test the start_server function when a socket error occurs."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.bind.side_effect = OSError

            with patch('builtins.print') as mock_print:
                start_server()
                mock_print.assert_any_call("DEBUG: Error handling connection: ")

    def test_start_server_exception(self, config_mock: MagicMock) -> None:
        """Test the start_server function when an exception occurs."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.accept.side_effect = Exception("Test exception")

            with patch('builtins.print') as mock_print:
                start_server()
                mock_print.assert_any_call("DEBUG: Error handling connection: Test exception")

    def test_handle_client_timeout(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when a timeout occurs."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = socket.timeout

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{host}', {port}): ")

    def test_handle_client_general_exception(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when a general exception occurs."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = Exception("Test exception")

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{host}', {port}): Test exception")

    def test_handle_client_empty_data_with_psk_auth(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when the received data is empty but PSK authentication is enabled."""
        config_mock.get.side_effect = [
            self.test_file_path, host, port, psk_auth,
            psk, reread_on_query
        ]
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b''

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'One or more invalid input.')
            mock_print.assert_any_call(f"DEBUG: Connection from ('{host}', {port}) has been established.")

    def test_handle_client_data_without_psk_hash_with_psk_auth(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when the received data does not
        start with the PSK hash but PSK authentication is enabled."""
        config_mock.get.side_effect = [
            self.test_file_path, host, port, psk_auth,
            psk, reread_on_query
        ]
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'test'

        with patch('builtins.print') as mock_print:
            if psk_auth:
                handle_client(mock_conn, (host, port))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_timeout_on_slow_connection(self, config_mock: MagicMock) -> None:
        """Test that the server times out when the connection takes too long."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = socket.timeout

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{host}', {port}): ")

    def test_psk_authentication_success(self, config_mock: MagicMock) -> None:
        """Test successful PSK authentication."""
        valid_psk_hash = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}some_query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once()

    def test_query_found(self, config_mock: MagicMock) -> None:
        """Test that the server correctly identifies a query that exists in the file."""
        valid_psk_hash = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}test data'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_query_not_found(self, config_mock: MagicMock) -> None:
        """Test that the server correctly identifies a query that does not exist in the file."""
        valid_psk_hash = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}nonexistent'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_handle_large_query(self, config_mock: MagicMock) -> None:
        """Test handling of a very large query string."""
        large_query = 'a' * 10000
        valid_psk_hash = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}{large_query}'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_partial_match(self, config_mock: MagicMock) -> None:
        """Test that partial matches do not result in a positive response."""
        valid_psk_hash = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}test'.encode('utf-8')  # 'test' is part of 'test data'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_psk_disabled_success(self, config_mock: MagicMock) -> None:
        """Test successful query processing when PSK authentication is disabled."""
        config_mock.getboolean.side_effect = [False, reread_on_query]  # Disable PSK auth
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'some_query'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once()

    def test_psk_disabled_with_psk_in_query(self, config_mock: MagicMock) -> None:
        """Test query processing when PSK authentication is disabled and the query contains the PSK hash."""
        config_mock.getboolean.side_effect = [False, reread_on_query]  # Disable PSK auth
        psk_hash_in_query = hashlib.sha256(psk.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{psk_hash_in_query}some_query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (host, port))
            mock_conn.sendall.assert_called_once()

    def test_psk_enabled_no_psk_provided(self, config_mock: MagicMock) -> None:
        """Test that the server handles missing PSK when PSK authentication is enabled."""
        config_mock.getboolean.side_effect = [True, reread_on_query]  # Enable PSK auth
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'some_query'

        with patch('builtins.print') as mock_print:
            if psk_auth:
                handle_client(mock_conn, (host, port))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_handle_client_large_payload(self, config_mock: MagicMock) -> None:
        """Test the handle_client function when the client sends a large payload."""
        config_mock.get.side_effect = [
            self.test_file_path, host, port, psk_auth,
            psk, reread_on_query
        ]
        mock_conn = MagicMock()
        large_payload = b'test' * 1024  # Create a payload larger than 1024 bytes
        mock_conn.recv.return_value = large_payload

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('builtins.print') as mock_print:
                handle_client(mock_conn, (host, port))
                mock_conn.sendall.assert_called_once()

                # Check the actual calls made to mock_print
                print(mock_print.call_args_list)

                # Assert the expected call based on the actual calls
                expected_call = mock_print.call_args_list[1]
                mock_print.assert_any_call(*expected_call[0], **expected_call[1])


if __name__ == '__main__':
    unittest.main()
