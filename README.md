## Project Description

This project is a simple server that listens for incoming connections and searches for a given string in a file. The server can be configured with various settings through a configuration file (`config.ini`).

## Configuration

The `config.ini` file contains the following settings:

- `FILE_PATH`: The path to the file to be searched.
- `HOST`: The hostname or IP address to bind the server.
- `PORT`: The port number to listen on.
- `PSK_AUTH`: A boolean value indicating whether Pre-Shared Key (PSK) authentication is enabled or not.
- `PSK`: The Pre-Shared Key value, if PSK authentication is enabled.
- `REREAD_ON_QUERY`: A boolean value indicating whether the file should be re-read from disk on every query or not.

## Usage

1. Configure the settings in the `config.ini` file as per your requirements.
2. Run the server script `python server.py`.
3. The server will start listening for incoming connections on the specified host and port.
4. To query the server, send a string to the server.
5. The server will search for the string in the specified file and respond with `"STRING EXISTS"` if found, or `"STRING NOT FOUND"` if not found.

## Features

- **PSK Authentication**: The server can be configured to require a Pre-Shared Key for authentication. If enabled, clients must prefix their queries with the PSK value.
- **Reread on Query**: The server can be configured to re-read the file from disk on every query or read the file once and store its contents in memory.
- **Logging**: The server logs various debug messages, such as the received query, the response sent, and the execution time.
- **Multi-threading**: The server can handle multiple client connections concurrently using threads.

## Project Structure

- project_resources/: This directory contains the source code of other tested algorithms and useful tools
- tests/: This directory contains the test cases implemented using pytest.
- config.ini: The configuration file containing various settings for the server.
- requirements.txt: Contains the required dependencies
- client.py: The client script, mainly for testing purpose
- server.py: The server script
- 250k.txt: The Text file to search for string

## Notes

- The server searches for an exact match of the provided string in the file.
- The server does not support partial matches or regular expressions.
- The server assumes the file encoding to be UTF-8.
- Error handling and exception handling are implemented to ensure graceful handling of errors and exceptions.

## Installation Instruction (LINUX)

Here's an installation guide on how to install and run the server as a Linux daemon:

1. Prerequisites
   - Make sure you have Python installed on your Linux system. This script is written in Python 3.11, so you'll need Python 3.11 or above installed.
   - Install the required Python packages if you haven't already.

2. Set up the Configuration File
   - Create a new file named config.ini in the same directory as your Python script.
   - Open the config.ini file, replace the values with your desired settings:
   - Replace file_path with the actual path to the file you want to serve.
   - Set the host and port values for your server.
   - Set psk_auth to True or False to enable or disable Pre-Shared Key (PSK) authentication.
   - If psk_auth is True, set psk to the desired PSK value.
   - Set reread_on_query to True or False to enable or disable re-reading the file for each query.

3. Copy the Python Script
   - Copy the provided Python script to a directory on your Linux system. For example, you can create a new directory /opt/myserver and copy the script there.
     
4. Create a Service File
   - Create a new service file for your Python script. This file will be used by systemd to manage the script as a daemon.
   - Create a new file named myserver.service in the /etc/systemd/system/ directory with the following content:
     [Unit]
     Description=My Python Server
     After=network.target

     [Service]
     ExecStart=/usr/bin/python3 /opt/myserver/server.py
     WorkingDirectory=/opt/myserver
     User=username
     Restart=always

     [Install]
     WantedBy=multi-user.target
   
   - Replace /opt/myserver/server.py with the actual path to your Python script.
   - Replace username with the user account you want to run the script under.
     

5.  Enable and Start the Service
    - After creating the service file, you need to enable and start the service:

     sudo systemctl daemon-reload
     sudo systemctl enable myserver.service
     sudo systemctl start myserver.service

    - The systemctl daemon-reload command reloads the systemd configuration
    - The systemctl enable myserver.service command enables the service to start automatically on system boot.
    - The systemctl start myserver.service command starts the service immediately.

6.  Verify the Service
    - To check the status of the service, run:

      sudo systemctl status myserver.service
     
    - This command will show you the current status of the service.
     
7. Logs and Troubleshooting
   - The script will log messages to the console. To view the logs, you can use the journalctl command:

      sudo journalctl -u myserver.service -f
     
   - This command will show you the logs for the myserver.service in real-time. Press Ctrl+C to exit.
   - If you encounter any issues, check the logs for error messages and try to resolve them accordingly.

With this setup, the server should now be running as a Linux daemon, managed by systemd. You can stop, start, or restart the service using the systemctl command:

    sudo systemctl stop myserver.service
    sudo systemctl start myserver.service
    sudo systemctl restart myserver.service






