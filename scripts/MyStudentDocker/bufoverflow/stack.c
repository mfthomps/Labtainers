/* stack.c */

/* Lab Exercise - Buffer Overflow */
/* This program has an buffer overflow vulnerability. */
/* Your task is to exploit this vulnerability */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int bof(char *str)
{
    char buffer[12];

    //BO Vulnerability
    strcpy(buffer,str);

    return 1;
}

int main(int argc, char* argv[])
{
    char str[517];

    FILE *badfile;
    badfile = fopen("badfile","r");

    fread(str, sizeof(char),517, badfile);
    bof(str);

    printf("Returned Properly\n");
    return 1;
}
