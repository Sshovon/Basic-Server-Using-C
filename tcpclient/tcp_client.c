#include <stdio.h>
#include <stdlib.h>

#include <sys/types.h>
#include <sys/socket.h>

#include <netinet/in.h>
#include <arpa/inet.h>


int main(){

    //creating socket

    int network_socket;
    network_socket=socket(AF_INET, SOCK_STREAM, 0);

    //specify an address for the socket of the remote server
    struct sockaddr_in server_address;

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(9002);  //htons is defined in <netinet/in.h> header
    server_address.sin_addr.s_addr = INADDR_ANY;

    int connection_status =connect(network_socket, (struct sockaddr *) &server_address, sizeof(server_address)); //casting server address    

    if(connection_status == -1){
        printf("connection failed\n\n");
    }

    char server_response [256];
    recv(network_socket, &server_response,sizeof(server_response),0);

    printf("%s\n",server_response);
    //close(network_socket);
    return 0;
}
