#include<stdio.h>
#include<stdlib.h>

int main(int argc, char *argv[])
{
    char user_input[100];
    int  var1 = 13;
    int  var2 = 21;
    char *str = "my dog has fleas";
    printf("var1 is: %d \n", var1);
    printf("var2 is: 0x%x and str is : %s\n", var2, str);
    printf("Enter a string:\n");
    scanf("%s", user_input);
    printf(user_input);
    printf("\n");
}
