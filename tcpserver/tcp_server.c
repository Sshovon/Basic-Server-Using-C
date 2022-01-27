#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <netinet/in.h>
#include <arpa/inet.h>

#define BACK_LOG 10

int main(){

    char server_message[256] = " Hello from server side";

    int server_socket;
    server_socket = socket(AF_INET,SOCK_STREAM,0);

    struct sockaddr_in server_address;

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(9002);
    server_address.sin_addr.s_addr = INADDR_ANY;


    bind(server_socket, (struct sockaddr*) &server_address, sizeof(server_address));

    listen(server_socket,BACK_LOG);

    int client_socket;

    client_socket= accept(server_socket,NULL, NULL); // this null is like accepting where is the client is connecting from if we provide a structure

    send(client_socket,server_message,sizeof(server_message),0);
    
    //close(server_socket);
    return  0;
}