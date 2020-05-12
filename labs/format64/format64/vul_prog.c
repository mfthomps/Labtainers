/* vul_prog.c */

#include<stdio.h>
#include<stdlib.h>

#define SECRET1 0x40
#define SECRET2 SECRET2_VALUE

int main(int argc, char *argv[])
{
    char user_input[100];
    int *secret;
    int *address_fix; /* hack to keep scanf delimiters out of addresses */
    long int int_input;  /* this was an int in formatstring; all other code is the same. */
    int a, b, c, d; /* other variables, not used here.*/
    
    /* The secret value is stored on the heap */
    address_fix = (int *) malloc(2*sizeof(int));
    secret = (int *) malloc(2*sizeof(int));
    
    /* getting the secret */
    secret[0] = SECRET1; secret[1] = SECRET2;
    
    printf("The variable secret's address is 0x%x (on stack)\n", (unsigned int)&secret);
    printf("The variable secret's value is 0x%x (on heap)\n", (unsigned int)secret);
    printf("secret[0]'s address is 0x%x (on heap)\n", (unsigned int)&secret[0]);
    printf("secret[1]'s address is 0x%x (on heap)\n", (unsigned int)&secret[1]);
    
    printf("Please enter a decimal integer\n");
    scanf("%d", &int_input);  /* getting an input from user */
    printf("Please enter a string\n");
    scanf("%s", user_input); /* getting a string from user */
    
    /* Vulnerable place */
    printf(user_input);
    printf("\n");
    
    /* Verify whether your attack is successful */
    printf("The original secrets: 0x%x -- 0x%x\n", SECRET1, SECRET2);
    printf("The new secrets:      0x%x -- 0x%x\n", secret[0], secret[1]);
    return 0;
}
