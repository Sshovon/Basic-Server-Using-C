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

    int sockfd,newsockfd,n;
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
    
    char c;
    FILE * fp;
    fp =fopen("webroot/index.asis","r");
    int cw=0;
    while(1){
        c=fgetc(fp);
        if(feof(fp)){
            break;
        }
        cw++;

    }
    write(newsockfd,&cw,sizeof(cw));
    rewind(fp);
    while(1){
        c=fgetc(fp);
        if(feof(fp)){
            break;
        }
        write(newsockfd,&c,sizeof(c));
    }

    printf("Done from server\n");

    close(sockfd);
    close(newsockfd);
    return 0;
}