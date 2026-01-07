import os, random, datetime, uuid

root_dir = "File_Server_Root"

# [1] 설정 파일 생성 (Config)
print(">> Generating System Configs...")
configs = ['nginx.conf', 'httpd.conf', 'sysctl.conf', 'fstab', 'hosts']
for cfg in configs:
    with open(f"{root_dir}/System/Config/{cfg}", "w") as f:
        f.write(f"# System Config Generated at {datetime.datetime.now()}\nserver_name localhost;\nlisten 80;\n")

# [2] 로그 파일 대량 생성 (Logs)
print(">> Generating Massive Logs...")
for i in range(1, 101): # 100개 로그
    with open(f"{root_dir}/Logs/Access/access_log_{i:03d}.log", "w") as f:
        f.write(f"192.168.1.{random.randint(1,255)} - - [{datetime.datetime.now()}] 'GET /index.html' 200\n" * 50)

# [3] 데이터베이스 덤프 (DB)
print(">> Generating SQL Dumps...")
for i in range(1, 21): # 20개 DB
    with open(f"{root_dir}/Database/Backups/db_backup_{datetime.date.today()}_{i}.sql", "w") as f:
        f.write(f"-- MySQL Dump {i}\nCREATE TABLE users_{i} (id INT, name VARCHAR(50));\nINSERT INTO users_{i} VALUES (1, 'Admin');\n")

# [4] 사용자 문서 (Users - Random Files)
print(">> Generating User Documents...")
exts = ['txt', 'md', 'json', 'xml', 'py', 'java', 'c']
for user in ['Admin', 'Developers']:
    for i in range(50):
        ext = random.choice(exts)
        fname = f"project_file_{uuid.uuid4().hex[:8]}.{ext}"
        with open(f"{root_dir}/Users/{user}/{fname}", "w") as f:
            f.write(f"// Content of {fname}\n// Created by {user}\n")

# [5] 시스템 커널 시뮬레이션
with open(f"{root_dir}/System/Kernels/vmlinuz-5.15.0-generic", "w") as f: f.write("BINARY_DATA_SIMULATION")

print("✅ Massive Files Generated Successfully.")
