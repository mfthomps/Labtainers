#include <stdio.h>
#include <stdlib.h>
void main(int argc, char *argv[]) {
    int total;
    int n;
    int i;
    /* Your edit goes below */
    	
    /* Add line above      */
    if(argc > 1) {
	i = atoi(argv[1]);
    }
    else {
	printf("You must provide one integer argument greater than 0.\n");
	i = -1;
    }
    for(n = 0; n <= i; n++) {
	if(n % 2 == 0){	
	    total += (n + n + 1) * n;
	}
	else{
	    total -= (n + n + 1) * n;
	}
    }
    total = abs(total);
    printf("The value of 1 should be 3.\nThe value of 2 should be 7.\nThe value of 3 should be 14.\nThe value of 4 should be 22.\nYour total is: %d\n", total);
}
	
        
