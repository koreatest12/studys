---
title: "DevOps Master Manual (Linux & Maven)"
author: "Auto-Generated System"
date: "2026-01-07"
geometry: margin=1in
mainfont: "NanumGothic"
---

# Chapter 1: Linux Basics
| Cmd | Desc |
|:---|:---|
| `ls -al` | List files details |
| `df -h` | Check disk space |

# Chapter 2: Database (SQLite)
This system auto-generates massive SQLite DBs every 10 mins.

# Chapter 3: GitHub Packages (Maven)
## Authentication
GitHub Packages supports only **Personal Access Token (Classic)**.
Edit `~/.m2/settings.xml` to include your credentials.

## Publishing (`mvn deploy`)
1. Edit `pom.xml` to add `<distributionManagement>`.
2. Ensure `<repository>` ID matches the server ID in `settings.xml`.
3. Run `mvn deploy`.

## Installing (`mvn install`)
Add the dependency to your `pom.xml`:
```xml
<dependency>
  <groupId>com.example</groupId>
  <artifactId>test</artifactId>
  <version>1.0.0-SNAPSHOT</version>
</dependency>
```

> **Note:** Artifact names must use lowercase, numbers, and hyphens.
