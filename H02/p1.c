#include <stdio.h>

unsigned long get_sp(void)
{
    __asm__("movl %esp,%eax");
}

int main()
{

    return 0;
}