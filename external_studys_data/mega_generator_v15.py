import os
import random
import datetime
import shutil
import sqlite3
import time

# === [1] 디스크 안전 감지 함수 (Crash 방지) ===
def is_disk_safe(min_gb=1.5):
    total, used, free = shutil.disk_usage("/")
    return (free / (1024**3)) > min_gb

# === [2] 서비스 메쉬 디렉토리 구조 생성 ===
base_dir = "Mega_Service_Mesh"
services = [
    "Auth_Server", "Payment_Cluster", "User_Node_A", 
    "User_Node_B", "Log_Vault", "Backup_Shard"
]

# 기존 데이터 정리 후 재생성 (중복 방지)
if os.path.exists(base_dir):
    shutil.rmtree(base_dir)
os.makedirs(base_dir, exist_ok=True)

# === [3] DB 테이블 대량 생성 ===
db_path = f"{base_dir}/enterprise_core.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

tables = ["access_logs", "transaction_history", "error_reports", "user_sessions"]
for tbl in tables:
    cursor.execute(f"CREATE TABLE IF NOT EXISTS {tbl} (id INTEGER PRIMARY KEY, data TEXT, created_at TIMESTAMP)")

print(">> 🚀 Generating Massive Data Shards...")

# === [4] 파일 및 레코드 대량 투입 ===
file_count = 0

for svc in services:
    svc_path = f"{base_dir}/{svc}"
    os.makedirs(svc_path, exist_ok=True)
    
    # 4-1. DB 레코드 대량 삽입
    for _ in range(100):
        cursor.execute(f"INSERT INTO access_logs (data, created_at) VALUES (?, ?)", 
                      (f"Access from {svc} node", datetime.datetime.now()))
    
    # 4-2. 파일 생성 (용량 체크하며 진행)
    if is_disk_safe():
        # 5개 ~ 10개의 중형 파일 생성
        for i in range(random.randint(5, 10)):
            # 파일 크기 5MB ~ 15MB (안전 범위 내 최대화)
            size_mb = random.randint(5, 15)
            fname = f"{svc_path}/shard_{i}_{int(time.time())}.bin"
            try:
                with open(fname, "wb") as f:
                    f.seek((size_mb * 1024 * 1024) - 1)
                    f.write(b'\0')
                file_count += 1
            except:
                break
    else:
        print(f"⚠️ Skipping large files for {svc} (Disk Limit Reached)")
        with open(f"{svc_path}/overflow_alert.txt", "w") as f:
            f.write("Disk Full - Generation Paused")

conn.commit()
conn.close()
print(f"✅ Generated {file_count} shards across {len(services)} services.")

# === [5] 어드민 대시보드 생성 ===
total, used, free = shutil.disk_usage("/")
used_gb = used // (1024**3)
total_gb = total // (1024**3)

html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>MEGA SERVER V15 STATUS</title>
    <style>
        body {{ background: #111; color: #0f0; font-family: 'Courier New'; padding: 20px; }}
        .box {{ border: 1px solid #0f0; padding: 15px; margin-bottom: 20px; }}
        h1 {{ text-align: center; border-bottom: 1px solid #0f0; }}
        .bar {{ background: #333; height: 20px; width: 100%; }}
        .fill {{ background: #0f0; height: 100%; width: {(used/total)*100}%; }}
    </style>
</head>
<body>
    <h1>🖥️ ULTRA SERVER V15 ONLINE</h1>
    <div class="box">
        <h3>💾 DISK STATUS (AUTO-MANAGED)</h3>
        <div class="bar"><div class="fill"></div></div>
        <p>{used_gb} GB Used / {total_gb} GB Total</p>
        <p>Generated Files: {file_count} Shards</p>
    </div>
    <div class="box">
        <h3>🔗 EXTERNAL INTEGRATION</h3>
        <p>Repository: koreatest12/studys (Integrated)</p>
        <p>Status: Active</p>
    </div>
    <div class="box">
        <h3>🛡️ AUTO-REPAIR LOG</h3>
        <p>Conflict Resolution: Executed</p>
        <p>Directory Clean: Completed</p>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
