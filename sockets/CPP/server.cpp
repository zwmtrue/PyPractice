#include <iostream>
#include <cstring>
#include <cstdio>
#include <cstdlib>
#include <vector>
#include <algorithm>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

using namespace std;

const int BUFFER_SIZE = 1024;

int main(int argc, char* argv[]) {
    if (argc != 2) {
        cerr << "Usage: " << argv[0] << " <port>" << endl;
        return EXIT_FAILURE;
    }

    int server_socket, client_socket, optval = 1;
    sockaddr_in server_address, client_address;
    socklen_t client_address_len = sizeof(client_address);
    char buffer[BUFFER_SIZE];

    // create socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        cerr << "Error: Failed to create socket." << endl;
        return EXIT_FAILURE;
    }

    // set socket options
    if (setsockopt(server_socket, SOL_SOCKET, SO_REUSEADDR, &optval, sizeof(optval)) < 0) {
        cerr << "Error: Failed to set socket options." << endl;
        return EXIT_FAILURE;
    }

    // bind to IP address and port
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(atoi(argv[1]));

    if (bind(server_socket, (sockaddr*)&server_address, sizeof(server_address)) < 0) {
        cerr << "Error: Failed to bind socket." << endl;
        return EXIT_FAILURE;
    }

    // start listening for client connections
    if (listen(server_socket, 5) < 0) {
        cerr << "Error: Failed to start listening." << endl;
        return EXIT_FAILURE;
    }

    // create client set
    fd_set clients;
    FD_ZERO(&clients);

    // add server socket to client set
    FD_SET(server_socket, &clients);

    // main loop to handle client connections and data transmission
    while (true) {
        // use select to monitor socket events
        fd_set read_fds = clients;
        if (select(FD_SETSIZE, &read_fds, NULL, NULL, NULL) < 0) {
            cerr << "Error: Failed to use select." << endl;
            return EXIT_FAILURE;
        }

        // handle client sockets
        for (int client_fd = 0; client_fd < FD_SETSIZE; client_fd++) {
            if (FD_ISSET(client_fd, &read_fds)) {
                if (client_fd == server_socket) {
                    // accept new client connections
                    if ((client_socket = accept(server_socket, (sockaddr*)&client_address, &client_address_len)) < 0) {
                        cerr << "Error: Failed to accept client." << endl;
                    }
                    else {
                        cout << "New client connected: " << inet_ntoa(client_address.sin_addr) << ":" << ntohs(client_address.sin_port) << endl;

                        // add client socket to client set
                        FD_SET(client_socket, &clients);
                    }
                }
                else {
                    // receive data from the client
                    int nbytes = recv(client_fd, buffer, BUFFER_SIZE, 0);
                    if (nbytes <= 0) {
                        // remove client socket from client set
                        close(client_fd);
                        FD_CLR(client_fd, &clients);

                        // report client disconnection
                        cout << "Client disconnected: " << inet_ntoa(client_address.sin_addr) << ":" << ntohs(client_address.sin_port) << endl;

