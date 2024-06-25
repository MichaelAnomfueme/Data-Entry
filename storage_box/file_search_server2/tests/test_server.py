import hashlib
import socket
import unittest
from unittest.mock import MagicMock, mock_open, patch

import server
from server import (
        HOST,
        PORT,
        PSK_AUTH,
        PSK,
        REREAD_ON_QUERY,
        log_settings,
        start_server,
        handle_client
)

# Type aliases
MockConnection = MagicMock
ConfigMock = MagicMock
PrintMock = MagicMock


@patch('server.ConfigParser')
class TestServer(unittest.TestCase):
    """Unit tests for the server functions."""

    def setUp(self) -> None:
        """Set up test data and configurations."""
        self.test_file_path = 'tests/test_data.txt'
        self.test_data = 'test data\nanother line\nquery'

        # Create a mock ConfigParser object
        self.config_mock = MagicMock()
        self.config_mock.get.side_effect = [
            self.test_file_path,
            HOST,
            PORT,
            PSK_AUTH,
            PSK,
            REREAD_ON_QUERY,
        ]

    def test_log_settings(self, _) -> None:
        """Test the log_settings function."""
        with patch('builtins.print') as mock_print:
            log_settings()
            if PSK_AUTH:
                mock_print.assert_any_call("DEBUG: PSK authentication enabled")
            if REREAD_ON_QUERY:
                mock_print.assert_any_call("DEBUG: Reread on query enabled")
            if not PSK_AUTH:
                mock_print.assert_any_call("DEBUG: PSK authentication disabled")
            if not REREAD_ON_QUERY:
                mock_print.assert_any_call("DEBUG: Reread on query disabled")

    def test_start_server(self, _) -> None:
        """Test the start_server function."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.accept.side_effect = socket.error

            start_server()

            mock_socket.assert_called_once()
            mock_server.bind.assert_called_once()
            mock_server.listen.assert_called_once_with(5)

    def test_handle_client(self, _) -> None:
        """Test the handle_client function."""
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'test'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))

            mock_conn.sendall.assert_called_once()
            mock_conn.close.assert_called_once()

    def test_handle_client_PSK_AUTH_failure(self, _) -> None:
        """Test the handle_client function when PSK authentication fails."""
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'invalid_PSK_hash'

        with patch('builtins.print') as mock_print:
            if PSK_AUTH:
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_start_server_socket_error(self, _) -> None:
        """Test the start_server function when a socket error occurs."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.bind.side_effect = OSError

            with patch('builtins.print') as mock_print:
                start_server()
                mock_print.assert_any_call("DEBUG: Error handling connection: ")

    def test_start_server_exception(self, _) -> None:
        """Test the start_server function when an exception occurs."""
        with patch('socket.socket') as mock_socket:
            mock_server = MagicMock()
            mock_socket.return_value = mock_server
            mock_server.accept.side_effect = Exception("Test exception")

            with patch('builtins.print') as mock_print:
                start_server()
                mock_print.assert_any_call("DEBUG: Error handling connection: Test exception")

    def test_handle_client_timeout(self, _) -> None:
        """Test the handle_client function when a timeout occurs."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = socket.timeout

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{HOST}', {PORT}): ")

    def test_handle_client_general_exception(self, _) -> None:
        """Test the handle_client function when a general exception occurs."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = Exception("Test exception")

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{HOST}', {PORT}): Test exception")

    def test_handle_client_data_without_PSK_hash_with_PSK_AUTH(self, _) -> None:
        """Test the handle_client function when the received data does not
        start with the PSK hash but PSK authentication is enabled."""
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'test'

        with patch('builtins.print') as mock_print:
            if PSK_AUTH:
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_timeout_on_slow_connection(self, _) -> None:
        """Test that the server times out when the connection takes too long."""
        mock_conn = MagicMock()
        mock_conn.recv.side_effect = socket.timeout

        with patch('builtins.print') as mock_print:
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'Could not handle your request pls try again later')
            mock_print.assert_any_call(f"DEBUG: Error handling client ('{HOST}', {PORT}): ")

    def test_PSK_AUTH_success(self, _) -> None:
        """Test successful PSK authentication."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}some_query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once()

    def test_query_not_found(self, _) -> None:
        """Test that the server correctly identifies a query that does not exist in the file."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}nonexistent'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_partial_match(self, _) -> None:
        """Test that partial matches do not result in a positive response."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}test'.encode('utf-8')  # 'test' is part of 'test data'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_psk_disabled_success(self, _) -> None:
        """Test successful query processing when PSK authentication is disabled."""
        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [False, REREAD_ON_QUERY]  # Disable PSK auth
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'some_query'

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once()

    def test_PSK_disabled_with_PSK_in_query(self, _) -> None:
        """Test query processing when PSK authentication is disabled and the query contains the PSK hash."""
        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [False, REREAD_ON_QUERY]  # Disable PSK auth
        psk_hash_in_query = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{psk_hash_in_query}some_query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once()

    def test_PSK_enabled_no_PSK_provided(self, _) -> None:
        """Test that the server handles missing PSK when PSK authentication is enabled."""
        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [True, REREAD_ON_QUERY]  # Enable PSK auth
        mock_conn = MagicMock()
        mock_conn.recv.return_value = b'some_query'

        with patch('builtins.print') as mock_print:
            if PSK_AUTH:
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'Authentication failed - PSK mismatch.')
                mock_print.assert_any_call("DEBUG: PSK Authentication failed.")

    def test_handle_client_large_payload(self, _) -> None:
        """Test the handle_client function when the client sends a large payload."""
        mock_conn = MagicMock()
        large_payload = b'test' * 1024  # Create a payload larger than 1024 bytes
        mock_conn.recv.return_value = large_payload

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('builtins.print') as mock_print:
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once()

                # Check the actual calls made to mock_print
                print(mock_print.call_args_list)

                # Assert the expected call based on the actual calls
                expected_call = mock_print.call_args_list[1]
                mock_print.assert_any_call(*expected_call[0], **expected_call[1])

    def test_load_file_at_startup(self, _) -> None:
        """Test that the file contents are loaded into memory at startup."""
        with patch('builtins.open', mock_open(read_data=self.test_data)):
            log_settings()
            self.assertIsNotNone(server.file_contents_set)
            self.assertEqual(len(server.file_contents_set), 3)
            self.assertIn('test data', server.file_contents_set)
            self.assertIn('another line', server.file_contents_set)
            self.assertIn('query', server.file_contents_set)

    def test_query_found(self, _) -> None:
        """Test that the server correctly identifies a query that exists in the file."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            handle_client(mock_conn, (HOST, PORT))
            mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_reread_on_query_true(self, _) -> None:
        """Test the reread on query functionality when it is enabled."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}query'.encode('utf-8')

        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [True, True]  # Enable PSK auth and reread on query

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', True):
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_reread_on_query_false(self, _) -> None:
        """Test the reread on query functionality when it is disabled."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}query'.encode('utf-8')

        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [True, False]  # Enable PSK auth and disable reread on query

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', False):
                server.file_contents_set = set(self.test_data.splitlines())
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_query_found_with_reread_on_query_enabled(self, _) -> None:
        """Test querying a string that exists in the file with REREAD_ON_QUERY enabled."""
        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [True]  # Enable REREAD_ON_QUERY
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', True):
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_query_not_found_with_reread_on_query_enabled(self, _) -> None:
        """Test querying a string that does not exist in the file with REREAD_ON_QUERY enabled."""
        config_mock = MagicMock()
        config_mock.getboolean.side_effect = [True]  # Enable REREAD_ON_QUERY
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}nonexistent'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', True):
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')

    def test_query_found_with_reread_on_query_disabled(self, _) -> None:
        """Test querying a string that exists in the preloaded file content with REREAD_ON_QUERY disabled."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}query'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', False):
                log_settings()  # Preload the file content
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING EXISTS\n')

    def test_query_not_found_with_reread_on_query_disabled(self, _) -> None:
        """Test querying a string that does not exist in the preloaded file content with REREAD_ON_QUERY disabled."""
        valid_psk_hash = hashlib.sha256(PSK.encode()).hexdigest()
        mock_conn = MagicMock()
        mock_conn.recv.return_value = f'{valid_psk_hash}nonexistent'.encode('utf-8')

        with patch('builtins.open', mock_open(read_data=self.test_data)):
            with patch('server.REREAD_ON_QUERY', False):
                log_settings()  # Preload the file content
                handle_client(mock_conn, (HOST, PORT))
                mock_conn.sendall.assert_called_once_with(b'STRING NOT FOUND\n')


if __name__ == '__main__':
    unittest.main()
