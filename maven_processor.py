import os, datetime, sqlite3

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

# [1] settings.xml 템플릿 생성 (GitHub Packages 인증용)
def generate_maven_settings():
    settings_content = """<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0
                      http://maven.apache.org/xsd/settings-1.0.0.xsd">

  <activeProfiles>
    <activeProfile>github</activeProfile>
  </activeProfiles>

  <profiles>
    <profile>
      <id>github</id>
      <repositories>
        <repository>
          <id>central</id>
          <url>https://repo.maven.apache.org/maven2</url>
        </repository>
        <repository>
          <id>github</id>
          <url>https://maven.pkg.github.com/OWNER/REPOSITORY</url>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>

  <servers>
    <server>
      <id>github</id>
      <username>YOUR_GITHUB_USERNAME</username>
      <password>YOUR_PERSONAL_ACCESS_TOKEN</password>
    </server>
  </servers>
</settings>"""
    
    with open("output_data/maven_templates/settings_template.xml", "w") as f:
        f.write(settings_content)

# [2] pom.xml 템플릿 생성 (배포 설정 포함)
def generate_pom_template():
    pom_content = """<project xmlns="http://maven.apache.org/POM/4.0.0"
  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
  <modelVersion>4.0.0</modelVersion>

  <groupId>com.example</groupId>
  <artifactId>github-packages-test</artifactId>
  <version>1.0.0-SNAPSHOT</version>

  <distributionManagement>
     <repository>
       <id>github</id>
       <name>GitHub OWNER Apache Maven Packages</name>
       <url>https://maven.pkg.github.com/OWNER/REPOSITORY</url>
     </repository>
  </distributionManagement>
</project>"""
    
    with open("output_data/maven_templates/pom_deploy_template.xml", "w") as f:
        f.write(pom_content)

# [3] 통합 매뉴얼 (Markdown) 생성 - Maven 가이드 포함
def generate_manual():
    md_path = "output_data/manuals/DevOps_Master_Guide.md"
    with open(md_path, "w") as f:
        f.write(f"""---
title: "DevOps Master Manual (Linux & Maven)"
author: "Auto-Generated System"
date: "{datetime.datetime.now().strftime('%Y-%m-%d')}"
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
""")

# [4] 웹 대시보드 업데이트
def update_web():
    file_list = []
    for root, dirs, files in os.walk("output_data"):
        for file in files:
            path = os.path.join(root, file).replace(os.sep, '/')
            stat = os.stat(os.path.join(root, file))
            size_kb = stat.st_size / 1024
            file_list.append({'name': file, 'path': path, 'time': stat.st_mtime, 'size': size_kb})
    
    file_list.sort(key=lambda x: x['time'], reverse=True)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>DevOps & Maven Center</title>
        <style>
            body {{ background: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ border-bottom: 2px solid #f78166; color: #f78166; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th {{ background: #161b22; padding: 10px; text-align: left; color: #79c0ff; }}
            td {{ padding: 10px; border-bottom: 1px solid #30363d; }}
            a {{ color: #58a6ff; text-decoration: none; }}
            .badge {{ padding: 3px 6px; border-radius: 4px; font-size: 0.8em; color: black; }}
            .xml {{ background: #f0883e; }} 
            .pdf {{ background: #ff7b72; }}
            .db {{ background: #238636; color: white; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>📦 Maven & Linux DevOps Center</h1>
            <p>Automated Templates, Manuals, and Database Logs</p>
            <table><tr><th>Time</th><th>Type</th><th>File</th><th>Download</th></tr>
    """
    for f in file_list:
        ext = f['name'].split('.')[-1]
        badge = "badge"
        if ext == 'xml': badge += " xml"
        elif ext == 'pdf': badge += " pdf"
        elif ext == 'db': badge += " db"
        
        html += f"<tr><td>{datetime.datetime.fromtimestamp(f['time'])}</td><td><span class='{badge}'>{ext.upper()}</span></td><td>{f['name']}</td><td><a href='{f['path']}' download>Download</a></td></tr>"
    html += "</table></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    generate_maven_settings()
    generate_pom_template()
    generate_manual()
    update_web()
