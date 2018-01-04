/* mypriv.c 
Simple example of dropping privileges within a
program that has been granted the
CAP_DAC_READ_SEARCH capability.
*/
#include <fcntl.h>
#include <sys/types.h>
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
#include <linux/capability.h>
#include <sys/capability.h>
int cap_disable(cap_value_t capflag);
int cap_enable(cap_value_t capflag);
int cap_drop(cap_value_t capflag);
int is_cap_set(cap_value_t capflag);
int main(void)
{
   if (is_cap_set(CAP_DAC_READ_SEARCH) == 0) {
      printf("CAP_DAC_READ_SEARCH capability is not set for this program\n");
      return -1;
   }
   if (open ("/etc/shadow", O_RDONLY) < 0)
       printf("(a) Open failed\n");
       /* Question (a): is the above open sucessful? why? */
   if (cap_disable(CAP_DAC_READ_SEARCH) < 0) return -1;
   if (open ("/etc/shadow", O_RDONLY) < 0)
       printf("(b) Open failed\n");
       /* Question (b): is the above open sucessful? why? */
   if (cap_enable(CAP_DAC_READ_SEARCH) < 0) return -1;
   if (open ("/etc/shadow", O_RDONLY) < 0)
      printf("(c) Open failed\n");
      /* Question (c): is the above open sucessful? why?*/
   if (cap_drop(CAP_DAC_READ_SEARCH) < 0) return -1;
   if (open ("/etc/shadow", O_RDONLY) < 0)
      printf("(d) Open failed\n");
      /* Question (d): is the above open sucessful? why?*/
   if (cap_enable(CAP_DAC_READ_SEARCH) == 0) return -1;
   if (open ("/etc/shadow", O_RDONLY) < 0)
      printf("(e) Open failed\n");
      /* Question (e): is the above open sucessful? why?*/
}
int is_cap_set(cap_value_t capflag)
{
   cap_t mycaps;
   mycaps = cap_get_proc();
   cap_flag_value_t cap_flags_value;
   cap_get_flag(mycaps, capflag, CAP_EFFECTIVE, &cap_flags_value);
   if(cap_flags_value == CAP_SET)
       return 1;
   else
       return 0;
}
int cap_disable(cap_value_t capflag)
{
   cap_t mycaps;
   mycaps = cap_get_proc();
   if (mycaps == NULL)
      return -1;
   if (cap_set_flag(mycaps, CAP_EFFECTIVE, 1, &capflag, CAP_CLEAR) != 0)
      return -1;
   if (cap_set_proc(mycaps) != 0)
      return -1;
   return 0;
}
int cap_enable(cap_value_t capflag)
{
   cap_t mycaps;
   mycaps = cap_get_proc();
   if (mycaps == NULL)
      return -1;
   if (cap_set_flag(mycaps, CAP_EFFECTIVE, 1, &capflag, CAP_SET) != 0)
      return -1;
   if (cap_set_proc(mycaps) != 0)
      return -1;
   return 0;
}
int cap_drop(cap_value_t capflag)
{
   cap_t mycaps;
   mycaps = cap_get_proc();
   if (mycaps == NULL)
      return -1;
   if (cap_set_flag(mycaps, CAP_EFFECTIVE, 1, &capflag, CAP_CLEAR) != 0)
      return -1;
   if (cap_set_flag(mycaps, CAP_PERMITTED, 1, &capflag, CAP_CLEAR) != 0)
      return -1;
   if (cap_set_proc(mycaps) != 0)
      return -1;
   return 0;
}
