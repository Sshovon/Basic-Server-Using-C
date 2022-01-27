#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>


int main(){
    int scok= socket(AF_INET,SOCK_STREAM,0);

    printf("%d\n",scok);

}