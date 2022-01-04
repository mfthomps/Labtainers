#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
extern char ** environ;
int main()
{
   char * argv[2];
   printf("Environment variables for execve:\n");
   argv[0] = "/usr/bin/env";
   argv[1] = NULL;
   execve("/usr/bin/env", argv, NULL);
   return 0 ;
}
