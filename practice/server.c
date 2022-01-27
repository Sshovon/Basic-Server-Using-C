#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <unistd.h>

#define BACK_LOG 5

void error(const char *msg){
    perror(msg);
    exit(1);
}

int main(int argc, char *argv[]){

    if(argc<2){
        fprintf(stderr,"Port no. not provide\n");
        exit(1);
    }

    int sockfd,newsockfd;
    char buffer[255];

    sockfd= socket(AF_INET,SOCK_STREAM,0);
    if(sockfd < 0){
        error("error opening socket.\n");
    }

    struct sockaddr_in serv_addr,cli_addr;
    //bzero((char *)&serv_addr,sizeof(serv_addr));

    int portno = atoi(argv[1]);
    
    serv_addr.sin_family=AF_INET;
    serv_addr.sin_addr.s_addr=INADDR_ANY;
    serv_addr.sin_port=htons(portno);

    if(bind(sockfd,(struct sockaddr *)&serv_addr,sizeof(serv_addr))<0){
        error("binding failed\n");
    }

    listen(sockfd,BACK_LOG);

    socklen_t clilen = sizeof(cli_addr);
    newsockfd = accept(sockfd, (struct sockaddr *)&cli_addr,&clilen);
    if (newsockfd < 0){
        error("error on accept\n");
    }
    int n;
    while(1){
        bzero(buffer,255);
        n=read(newsockfd,buffer , 255);
        if(n<0){
            error("error on reading\n");
        }
        printf("Client : %s\n",buffer);
        bzero(buffer,255);
        fgets(buffer,255,stdin);

        n= write(newsockfd,buffer,strlen(buffer));
        if(n<0){
            error("error on writing.\n");
        }
        int cmp= strncmp("bye",buffer,3);
        if(!cmp) break;

    }

    close(sockfd);
    close(newsockfd);
    return 0;
}