#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
int main() {
    pid_t pid = fork();
    if (pid > 0) {
        // 부모 프로세스: 자식 종료를 기다리지 않고 10초간 대기 (자식은 좀비화)
        sleep(10);
    } else {
        // 자식 프로세스: 즉시 종료
        exit(0);
    }
    return 0;
}
