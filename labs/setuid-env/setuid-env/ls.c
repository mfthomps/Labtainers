/*
   ls program
*/
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
int main(){
    uid_t euid = geteuid();
    printf("my ls prog, euid is %d\n", euid);
    return 0;
}
