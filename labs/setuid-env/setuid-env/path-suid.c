#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
int main()
{
   uid_t euid = geteuid();
   printf("euid is %d\n", euid);
   system("ls");
   return 0;
}
