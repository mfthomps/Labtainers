#include <stdio.h>
void main() {
    int num;
    int count;
    int total;
    total = 0;
    num = 6;
    count = 15;
    while(count > 0) { /* Modify this line only */
	total = count / num;
	printf("%d divided by %d is: %d\n", count, num, total);
	count--;
	num--;
    }
}
