#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>


void error(const char *msg){
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[]){
    int sockfd,newsockfd,portno,n;
    char buffer[255];

    //char * address;
    //address=argv[1];
    portno=atoi(argv[1]);
    sockfd = socket(AF_INET,SOCK_STREAM,0);

    struct sockaddr_in serv_addr;
    //bzero((char *)&serv_addr,sizeof(serv_addr));
    serv_addr.sin_family=AF_INET;
    serv_addr.sin_addr.s_addr=INADDR_ANY;
    //inet_aton(address, &serv_addr.sin_addr.s_addr); //storing address 
    serv_addr.sin_port=htons(portno);

    connect(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr));
    
    while(1){
        bzero(buffer,255);
        fgets(buffer,255,stdin);
        n= write(sockfd,buffer,strlen(buffer));
        if(n<0){
            printf("error on writing.\n");
        }
        
        bzero(buffer,255);
        n=read(sockfd,buffer , 255);
        if(n<0){
            error("error on reading\n");
        }
        
        printf("Server: %s\n",buffer);
        
        int cmp= strncmp("bye",buffer,3);
        if(!cmp) break;

    }
    close(sockfd);

}