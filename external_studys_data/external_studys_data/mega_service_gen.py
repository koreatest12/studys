import os, random, time, datetime, shutil

# 기본 경로 설정
base_dir = "Service_Storage"
services = ["Web_Server", "DB_Cluster", "Auth_System", "Backup_Vault"]

# 디렉토리 구조 생성
for svc in services:
    os.makedirs(f"{base_dir}/{svc}", exist_ok=True)

print(">> 🚀 Starting Massive Data Generation per Service...")

# [1] 서비스별 데이터 분할 생성
total_generated_size = 0

for svc in services:
    # 서비스별로 3~5개의 대용량 파일 생성
    file_count = random.randint(3, 5)
    print(f"   -> Processing Service: {svc} ({file_count} files)")
    
    for i in range(file_count):
        # 파일 크기: 20MB ~ 60MB (랜덤)
        size_mb = random.randint(20, 60)
        fname = f"{svc}_data_{datetime.datetime.now().strftime('%H%M%S')}_{i}.bin"
        fpath = f"{base_dir}/{svc}/{fname}"
        
        # 더미 데이터 생성 (고속 쓰기)
        with open(fpath, "wb") as f:
            f.seek((size_mb * 1024 * 1024) - 1)
            f.write(b'\0')
        
        total_generated_size += size_mb

print(f"✅ Generated {total_generated_size} MB across {len(services)} services.")

# [2] 통합 대시보드 생성 (외부 데이터 포함)
def scan_files(start_dir):
    file_list = []
    for root, dirs, files in os.walk(start_dir):
        for file in files:
            path = os.path.join(root, file)
            size = os.path.getsize(path)
            file_list.append((file, path, size, os.path.getmtime(path)))
    return file_list

# 내부 생성 파일 + 외부(Studys) 파일 스캔
local_files = scan_files(base_dir)
ext_files = scan_files("external_studys_data")

all_files = sorted(local_files + ext_files, key=lambda x: x[3], reverse=True)[:50] # 최신 50개

# 디스크 정보
total, used, free = shutil.disk_usage("/")
used_gb = used // (1024**3)
total_gb = total // (1024**3)
used_percent = (used / total) * 100

html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset='utf-8'>
    <title>Ultra Mega Server V10 Admin</title>
    <style>
        body {{ background: #0d1117; color: #c9d1d9; font-family: sans-serif; padding: 20px; }}
        .status-card {{ border: 1px solid #30363d; padding: 20px; border-radius: 6px; background: #161b22; margin-bottom: 20px; }}
        h1 {{ color: #58a6ff; border-bottom: 1px solid #30363d; padding-bottom: 10px; }}
        h3 {{ color: #7ee787; }}
        
        /* Progress Bar */
        .progress-container {{ background: #30363d; height: 30px; border-radius: 15px; overflow: hidden; }}
        .progress-fill {{ background: linear-gradient(90deg, #238636, #3fb950); height: 100%; width: {used_percent}%; }}
        
        table {{ width: 100%; border-collapse: collapse; margin-top: 15px; font-size: 0.9em; }}
        th {{ background: #21262d; color: #f0f6fc; text-align: left; padding: 10px; }}
        td {{ border-bottom: 1px solid #30363d; padding: 10px; }}
        a {{ color: #58a6ff; text-decoration: none; }}
        .tag {{ display: inline-block; padding: 2px 8px; border-radius: 10px; font-size: 0.8em; font-weight: bold; }}
        .tag-local {{ background: #1f6feb; color: white; }}
        .tag-ext {{ background: #d29922; color: black; }}
    </style>
</head>
<body>
    <div class="status-card">
        <h1>🖥️ SYSTEM STATUS: ONLINE (V10)</h1>
        <p><b>Last Reboot:</b> {datetime.datetime.now()}</p>
        
        <h3>💾 Storage Capacity (Expanded)</h3>
        <div class="progress-container">
            <div class="progress-fill"></div>
        </div>
        <p style="text-align: right;">{used_gb} GB Used / {total_gb} GB Total ({used_percent:.1f}%)</p>
    </div>

    <div class="status-card">
        <h3>📂 Data File Explorer (Top 50 Recent)</h3>
        <p>Includes Generated Service Data & External Repository (Studys)</p>
        <table>
            <thead><tr><th>Source</th><th>Filename</th><th>Size</th><th>Download</th></tr></thead>
            <tbody>
"""

for fname, fpath, fsize, mtime in all_files:
    size_str = f"{fsize/1024/1024:.2f} MB" if fsize > 1024*1024 else f"{fsize/1024:.2f} KB"
    tag_class = "tag-ext" if "external_studys" in fpath else "tag-local"
    tag_name = "EXT_REPO" if "external_studys" in fpath else "LOCAL_GEN"
    
    # 다운로드 링크 처리를 위해 상대 경로 계산
    rel_path = os.path.relpath(fpath, os.getcwd())
    
    html_content += f"""
        <tr>
            <td><span class="tag {tag_class}">{tag_name}</span></td>
            <td>{fname} <br><span style="color:#8b949e; font-size:0.8em;">{rel_path}</span></td>
            <td>{size_str}</td>
            <td><a href="{rel_path}">⬇️ Access</a></td>
        </tr>
    """

html_content += """
            </tbody>
        </table>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)
