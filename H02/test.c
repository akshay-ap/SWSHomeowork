#include <stdio.h>
#include <string.h>

void exploitable(char *input)
{
    char buffer[512];
    printf("Address of buffer in exploitable program: %08x\n", buffer);
    strcpy(buffer, input);
}

int main(int argc, char *argv[])
{

    if (argc > 1)
        exploitable(argv[1]);
}
