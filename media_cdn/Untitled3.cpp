#include<stdio.h>
#include<stdlib.h>

int main()
{
	int i=320;
	char *ptr = (char*)&i;
	printf("%d",*ptr);
	return 0;
}
