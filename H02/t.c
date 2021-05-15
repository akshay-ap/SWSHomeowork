#include <stdio.h>

unsigned long get_sp(void)
{
    __asm__("movl %esp,%eax");
}

int main()
{
    int start_address = get_sp();
    printf("0x%x\n", start_address);
}
