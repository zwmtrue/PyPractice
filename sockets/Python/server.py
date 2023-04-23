# -*- coding: utf-8 -*-
"""
Created on Sun Apr 23 09:16:33 2023

@author: zwmtrue
"""
import socket
import select

# define server parameters
IP_ADDRESS = "127.0.0.1"
PORT = 8000
BUFFER_SIZE = 1024

# create a dictionary to store connected clients
clients = {}

# create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# set socket options and bind to IP address and port
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((IP_ADDRESS, PORT))

# start listening for client connections
server_socket.listen()

print(f"Server listening on {IP_ADDRESS}:{PORT}...")

# function to broadcast status updates to all subscribed clients
def broadcast(data):
    for client_socket in clients.values():
        client_socket.send(data)

# main loop to handle client connections and data transmission
while True:
    # use select to monitor socket events
    read_sockets, _, exception_sockets = select.select([server_socket] + list(clients.keys()), [], [server_socket])

    # handle exception sockets
    for exception_socket in exception_sockets:
        # remove the client from the dictionary
        del clients[exception_socket]

    # handle read sockets
    for read_socket in read_sockets:
        if read_socket == server_socket:
            # accept new client connections
            client_socket, client_address = server_socket.accept()
            print(f"New client connected: {client_address}")

            # add the new client to the dictionary
            clients[client_socket] = client_socket
        else:
            # receive data from the client
            data = read_socket.recv(BUFFER_SIZE)

            if data:
                # broadcast the data to all subscribed clients
                broadcast(data)
            else:
                # remove the client from the dictionary if no data received
                del clients[read_socket]
                print(f"Client disconnected: {read_socket.getpeername()}")
