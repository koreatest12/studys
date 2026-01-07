#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
int main() {
  printf("Spawning Process...\n");
  pid_t pid = fork();
  if (pid > 0) {
    printf("Parent (PID %d) Sleeping...\n", getpid());
    sleep(5);
    printf("Parent Waking Up.\n");
  } else {
    printf("Child (PID %d) Exiting (Zombie Mode)...\n", getpid());
    exit(0);
  }
  return 0;
}
