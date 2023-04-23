# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:19:39 2023

@author: zwmtrue
"""
import socket

# define server parameters
IP_ADDRESS = "127.0.0.1"
PORT = 8000
BUFFER_SIZE = 1024

# create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# connect to the server
client_socket.connect((IP_ADDRESS, PORT))
print(f"Connected to server: {IP_ADDRESS}:{PORT}")

# receive status updates from the server
while True:
    try:
        data = client_socket.recv(BUFFER_SIZE)
        if data:
            status_update = data.decode()
            print(f"New status update: {status_update}")
        else:
            print("Connection closed by server.")
            client_socket.close()
            break
    except KeyboardInterrupt:
        print("Closing connection...")
        client_socket.close()
        break
    except:
        print("Error: Failed to receive data.")
        client_socket.close()
        break
