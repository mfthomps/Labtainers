#include <stdio.h> 
int main(int argc, char * argv[]) 
{ 
    char string[100]; 
    int c = 0, count[26] = {0}; 
    printf("Enter a string:\n"); 
    gets(string); 
    while ( string[c] != '\0' ) 
    { 
       if ( string[c] >= 'a' && string[c] <= 'z' ) 
          count[string[c]-'a']++; 
       c++; 
    } 
    for ( c = 0 ; c < 26 ; c++ ) 
    { 
       if ( count[c] != 0 ) 
          printf("%d %d.\n",c+'a',count[c]); 
    } 
    return 0; 
}
