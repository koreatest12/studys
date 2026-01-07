#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
int main() {
    if (fork() > 0) sleep(10);
    else exit(0);
    return 0;
}
