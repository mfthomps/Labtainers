#include <stdio.h>
#include <stdlib.h>
int main()
{
    printf("Environment variables for system:\n");
    system("/usr/bin/env");
    return 0 ;
}
