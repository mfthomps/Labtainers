#include<stdio.h>
#include<stdlib.h>
#include<string.h>
/*
 *  Program to illustrate data references that overrun intended bounds.
 *  Compile this with gcc -m32 -g -o mystuff mystuff.c
 */
/*
 * Structure for holding my information.
 */
struct myData{
     char public_info[20]; // publicly available stuff
     char fav_color[BUF_SIZE];
     int pin;  // my pin
     int age;  // my age
};
/*
 * Initialize my information values.
 */
void setData(struct myData *data){
	strcpy(data->public_info, "I yam what I yam.");
	strcpy(data->fav_color, "red");
	data->pin = 99;
	data->age = 61;
}

void showMemory(struct myData data){
    /* temporary variables */
    int offset;
    int result;
    /* Show memory values at offsets into the public data field */
    while(1){
        printf("Enter an offset into your public data and we'll show you the character value.\n(or q to quit)\n");
        result = scanf("%d", &offset);
	if(result == 0){
		break;
	}
        printf("Hex value at offset %d (address 0x%p) is 0x%x\n", offset, &data.public_info[offset], data.public_info[offset]);
    }
}
void handleMyStuff(){
    /* Declare myData variable my_data */
    struct myData my_data;

    /* Initialized my_data */
    setData(&my_data);

    /* Display address of my_data fields */
    printf("Adress of public data:\t\t0x%p\nAddress of secret PIN:\t\t0x%p\n", &my_data.public_info[0], &my_data.pin);
    printf("\n\n");

    /* Display values of my_data fields */
    printf("Public data is %s\n",  my_data.public_info);
    printf("Hex value of PIN is 0x%x\n", my_data.pin);
    printf("\n\n");
    showMemory(my_data);
}
int main(int argc, char *argv[])
{
    handleMyStuff();
    printf("\nBye\n");
}
