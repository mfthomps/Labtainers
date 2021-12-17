#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <stdlib.h>
extern char ** environ;
void printenv()
{
   int i = 0;
   while (environ[i] != NULL) {
      printf("%s\n", environ[i]);
      i++;
   }
}
void main()
{
   pid_t childPid;
   printf("Environment variables for fork:\n");
   switch(childPid = fork()) {
      case 0:  /* child process */
         printenv();
         exit(0);
      default:  /* parent process */
         //printenv();
         exit(0);
   }
}
