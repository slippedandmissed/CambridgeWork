#include <stdio.h>

char *greetings(void) { return "Hello, world\n"; }
int main()
{
	char *p = greetings();
	p[0] = 'G';
	puts(p);
}
