---
title: "Linux System Manual"
author: "Automated System"
date: "2026-01-07"
geometry: margin=1in
mainfont: "NanumGothic"
---
# [Linux] System & Security Guide

## 1. Essential Commands
| Command | Description | Example |
|:---|:---|:---|
| **ls** | List Files | `ls -al` |
| **chmod** | Permissions | `chmod 755 file` |

## 2. Security Ops
| Command | Description | Example |
|:---|:---|:---|
| **passwd** | Change PW | `passwd user` |
| **chpasswd** | Batch PW | `echo "u:p" \| chpasswd` |

## 3. Process Code (Zombie)
```c
#include <stdlib.h>
#include <unistd.h>
int main() {
   if(fork()>0) sleep(10); 
   else exit(0);
   return 0;
}
```


_Generated: Wed Jan  7 12:55:58 UTC 2026_
