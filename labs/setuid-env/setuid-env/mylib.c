#include <stdio.h>
void sleep (int s)
{
   /* If this is invoked by a privileged program, you can do damage here!  */
   printf("I am not sleeping!\n");
}
