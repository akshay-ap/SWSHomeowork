#include <stdio.h>
void blub(int c)
{
    int d[2];
    d[1] = 23;
    d[0] = d[1] - 15;
    printf("%d", d[0]);
    return;
}
int main()
{

    blub(1);
    return 0;
}
