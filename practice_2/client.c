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
    
    bzero(buffer,255);
    int cw,i=0;
    char c;
    FILE * fp;
    fp =fopen("webroot/output.asis","a");

    read(sockfd,&cw,sizeof(cw));
    //printf("%d\n",cw);
    while(i!=cw){
        read(sockfd,&c,sizeof(c));
        //char x=(char)c;
        printf("%c",c);
        fprintf(fp,"%c",c);
        i++;
    }

    printf("Done from client\n");
    close(sockfd);

}