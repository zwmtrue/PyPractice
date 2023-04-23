#include <iostream>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <unistd.h>
#include <sys/socket.h>
#include <arpa/inet.h>

using namespace std;

const int BUFFER_SIZE = 1024;

int main(int argc, char* argv[]) {
    if (argc != 3) {
        cerr << "Usage: " << argv[0] << " <ip_address> <port>" << endl;
        return EXIT_FAILURE;
    }

    int client_socket;
    sockaddr_in server_address;
    char buffer[BUFFER_SIZE];

    // create socket
    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        cerr << "Error: Failed to create socket." << endl;
        return EXIT_FAILURE;
    }

    // connect to server
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = inet_addr(argv[1]);
    server_address.sin_port = htons(atoi(argv[2]));

    if (connect(client_socket, (sockaddr*)&server_address, sizeof(server_address)) < 0) {
        cerr << "Error: Failed to connect to server." << endl;
        return EXIT_FAILURE;
    }

    cout << "Connected to server: " << argv[1] << ":" << argv[2] << endl;

    // receive status updates from the server
    while (true) {
        int nbytes = recv(client_socket, buffer, BUFFER_SIZE, 0);
        if (nbytes <= 0) {
            cerr << "Error: Failed to receive data from server." << endl;
            break;
        }
        cout << "New status update: " << buffer << endl;
    }

    close(client_socket);
    return EXIT_SUCCESS;
}
