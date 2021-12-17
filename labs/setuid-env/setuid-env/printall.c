#include <stdio.h>
#include <stdlib.h>
extern char ** environ;
void main()
{
   printf("Environment variables from printall.\n");
   int i = 0;
   while (environ[i] != NULL) {
      printf("%s\n", environ[i]);
      i++;
   }
}
