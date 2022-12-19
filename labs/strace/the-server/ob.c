#include <stdio.h>
#include <string.h>
#include <sys/socket.h>
#include <arpa/inet.h>
#include <stdlib.h>
#define MAXLINE 1024
//#define MY_PORT_NUMBER 1024
int startshi(char *buffer){
    char *hi = "HI";
    if(strlen(buffer)>1 && buffer[0] == hi[0] && buffer[1] == hi[1]){
        return 1;
    }else{
        return 0;
    }
}
void main(){
    FILE *log = fopen("/tmp/log.txt", "w");
    srand(MY_PORT_NUMBER);
    int port = 10000 + (rand() % 2000);
    fprintf(log, "port is %d\n", port);
    fflush(log);
    int sock_fd, len, n;
    struct sockaddr_in servaddr, cliaddr;
    char *hello = "Yup, that is the port number!\n";
    char buffer[MAXLINE];
    if ( (sock_fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
        fprintf(log, "socket create failed.");
        exit(1);
    }
    memset(&servaddr, 0, sizeof(servaddr));
    memset(&cliaddr, 0, sizeof(cliaddr));
    servaddr.sin_family = AF_INET;
    servaddr.sin_addr.s_addr = INADDR_ANY;
    servaddr.sin_port = htons(port);
    FILE *config = fopen("/var/run/config.txt", "r");
    if (config == NULL) {
        fprintf(log, "Error opening config file\n");
        exit(EXIT_FAILURE);
    }
    int min_level = 0;
    int max_level = 0;
    int count = fscanf(config, "%d %d", &min_level, &max_level);
    if(count != 2 || min_level > max_level){
        fprintf(log, "bad levels, format: \nl1 l2\nWhere l1 is less than l2\n");
        exit(EXIT_FAILURE);
    }
    if ( bind(sock_fd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
        fprintf(log, "bind failed");
        exit(1);
    }
    char *server_name = "the-server";
    FILE *host_file = fopen("/etc/hostname", "r");
    fread(buffer, sizeof(buffer), 1, host_file);
    if(strncmp(buffer, server_name, strlen(server_name) ) != 0){
        fprintf(log, "Not the right host.\n");
        exit(EXIT_FAILURE);
    }
    len = sizeof(cliaddr);
    while(1){     
        n = recvfrom(sock_fd, (char *)buffer, MAXLINE, MSG_WAITALL, ( struct sockaddr *) &cliaddr, &len); 
        if(n == 0){
            close(sock_fd);
            sleep(5);
            if ( (sock_fd = socket(AF_INET, SOCK_DGRAM, 0)) < 0 ) {
                fprintf(log, "socket create failed.");
                exit(1);
            }
            if ( bind(sock_fd, (const struct sockaddr *)&servaddr, sizeof(servaddr)) < 0){
                fprintf(log, "bind failed");
                exit(1);
            }
            continue;
        }
        buffer[n] = '\0';
        fprintf(log, "got: %s\n", buffer);
        if(startshi(buffer)){ 
            sendto(sock_fd, (const char *)hello, strlen(hello), MSG_CONFIRM, (const struct sockaddr *) & cliaddr, len);
            fprintf(log, "sent msg\n");
        }
        fflush(log);
    }
}
