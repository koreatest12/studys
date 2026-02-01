#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
int main() {
  printf("Process Started...\n");
  pid_t pid = fork();
  if (pid > 0) {
    sleep(5);
  } else {
    exit(0);
  }
  return 0;
}
