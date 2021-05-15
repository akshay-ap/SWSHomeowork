#include <stdio.h>

void bin(unsigned n)
{
    /* step 1 */
    if (n > 1)
        bin(n / 2);

    /* step 2 */
    printf("%d", n % 2);
}

int main()
{
    int x;
    unsigned char u;
    signed char s;
    x = 'K' + 'S' + 'A';
    printf("x = %d\nmod = %d\n", x, (x % 127));
    s = (x % 127) + 128;
    u = (x % 127) + 128;
    printf("Signed: %d\n", s);
    printf("Unsigned: %d\n", u);
    bin(s);
    printf("\n");
    bin(u);
    printf("\n");
    return 0;
}
