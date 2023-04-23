# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:19:29 2023

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

# send status updates to the server
while True:
    try:
        status_update = input("Enter status update: ")
        client_socket.send(status_update.encode())
    except KeyboardInterrupt:
        print("Closing connection...")
        client_socket.close()
        break
    except:
        print("Error: Failed to send data.")
        client_socket.close()
        break