/* stack.c */

/* Lab Exercise - Buffer Overflow */
/* This program has an buffer overflow vulnerability. */
/* Your task is to exploit this vulnerability */

#include <stdlib.h>
#include <stdio.h>
#include <string.h>
int bof(char *str)
{
    char buffer[BUFFER_SIZE]; /* originally 12 in SEED labs */

    //BO Vulnerability
    strcpy(buffer,str);

    return 1;
}

int main(int argc, char* argv[])
{
    char str[1000]; /* originally 517 in SEED labs */

    FILE *badfile;
    badfile = fopen("badfile","r");

    fread(str, sizeof(char),1000, badfile); /* originally 517 in SEED labs */
    bof(str);

    printf("Returned Properly\n");
    return 1;
}
