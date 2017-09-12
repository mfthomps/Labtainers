#include <stdio.h>
#include <stdlib.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <signal.h>

#define FILEPATH "/tmp/iodevice"
#define NUMINTS  (1000)
#define FILESIZE (NUMINTS * sizeof(int))
#define FILE_ID "MY_FILE_ID"
void signal_handler(int signo)
{
    if (signo == SIGINT)
    {
        printf("caught SIGNINT, exit\n");
        exit(1);
    }
}
int main(int argc, char *argv[])
{
    int i;
    int fd;
    int result;
    int *map;  /* mmapped array of int's */
    if(signal(SIGINT, signal_handler) == SIG_ERR)
    {
        fprintf(stderr, "failed setting up signals\n");
        exit(1);
    }
    /* Open a file for writing.
     *  - Creating the file if it doesn't exist.
     * Note: "O_WRONLY" mode is not sufficient when mmaping.
     */
    printf("PLC starting, simulated IO on mapped file: %s\n", FILEPATH);
    fd = open(FILEPATH, O_RDWR, (mode_t)0600);
    if (fd == -1) {
        perror("Error opening file for writing");
        exit(EXIT_FAILURE);
    }
    /* Now the file is ready to be mmapped.
     */
    printf("do mmap \n");
    map = mmap(0, FILESIZE, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0);
    if (map == MAP_FAILED) {
        close(fd);
        printf("Error mmapping the file, fid is %s\n", FILE_ID);
        exit(EXIT_FAILURE);
    }
    printf("done mmap \n");
    /* mmap[0] is water level
       mmap[1] is pump, 1 for on, 0 for off */
    FILE *config = fopen("config.txt", "r");
    printf("done fopen config \n");
    if (config == NULL) {
        printf("Error opening config file\n");
        exit(EXIT_FAILURE);
    }
    int min_level = 0;
    int max_level = 0;
    //printf("do scan \n");
    fscanf(config, "%d %d", &min_level, &max_level);
    //printf("done scan \n");
    while(1)
    {
       int current_level = map[0];
       if(current_level > max_level)
       {
          map[1] = 1;
       }else if(current_level < min_level){
          map[1] = 0;
       }
       //printf("map 0 is %d\n", map[0]);
       //printf("map 1 is %d\n", map[1]);
       sleep(1);
    }
}

