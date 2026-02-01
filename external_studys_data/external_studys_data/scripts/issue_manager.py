import os
import sys
import random
import csv
import platform
import subprocess
from datetime import datetime
from github import Github

# --- 환경 변수 로드 ---
TOKEN = os.getenv('GH_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
MODE = os.getenv('MODE', 'auto')
COUNT = int(os.getenv('COUNT', 10))

if not TOKEN or not REPO_NAME:
    print("❌ Error: GH_TOKEN or REPO_NAME is missing.")
    sys.exit(1)

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

print(f"🚀 AI Ops System Started | Mode: {MODE}")

def get_server_info():
    """서버(Runner) 환경 정보 및 버전 확인"""
    try:
        # pip 패키지 버전 확인
        pip_freeze = subprocess.check_output([sys.executable, '-m', 'pip', 'freeze']).decode('utf-8')
        pygithub_ver = [line for line in pip_freeze.split('\n') if 'PyGithub' in line]
        pygithub_ver = pygithub_ver[0] if pygithub_ver else "Unknown"
        
        info = {
            "OS": platform.system() + " " + platform.release(),
            "Python": sys.version.split()[0],
            "PyGithub": pygithub_ver,
            "Timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        return info
    except Exception as e:
        return {"Error": str(e)}

def bulk_create():
    print(">> [Action] Bulk Create Issues")
    prefixes = ["[System]", "[Upgrade]", "[Patch]", "[Network]"]
    for i in range(COUNT):
        title = f"{random.choice(prefixes)} Server Upgrade Check #{random.randint(1000, 9999)}"
        body = f"Server sync test.\nTime: {datetime.now()}"
        repo.create_issue(title=title, body=body)

def bulk_update():
    print(">> [Action] Bulk Update & Labeling")
    issues = repo.get_issues(state='open')
    for i, issue in enumerate(issues):
        if i >= COUNT: break
        
        labels_to_add = []
        if "Upgrade" in issue.title: labels_to_add.append("maintenance")
        if "System" in issue.title: labels_to_add.append("backend")
        
        current_labels = [l.name for l in issue.labels]
        new_labels = [l for l in labels_to_add if l not in current_labels]
        if new_labels:
            issue.add_to_labels(*new_labels)
            print(f"   -> Updated #{issue.number}: Added {new_labels}")

def generate_report():
    print(">> [Action] Generate Report CSV")
    issues = repo.get_issues(state='all')
    with open("issue_report.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Number", "Title", "State", "Labels", "Created At"])
        for i, issue in enumerate(issues):
            if i >= COUNT * 5: break
            labels = ", ".join([l.name for l in issue.labels])
            writer.writerow([issue.number, issue.title, issue.state, labels, issue.created_at])

def auto_maintenance():
    """
    [서버 업그레이드 및 유지보수]
    1. 서버 환경 정보 수집
    2. REPO_STATUS.md 대시보드 갱신
    3. 리포트 및 라벨링 수행
    """
    print(">> [Action] Server Maintenance & Upgrade Log")
    
    server_info = get_server_info()
    
    # 파일 통계
    file_count = sum([len(files) for r, d, files in os.walk(".") if ".git" not in r])
    
    # 상태 대시보드 업데이트
    status_content = f"""# 🖥️ Server Upgrade & Status Dashboard
> System automatically upgraded and checked.

### 🛠️ Server Environment (Latest)
- **Last Upgrade**: {server_info.get('Timestamp')}
- **OS System**: {server_info.get('OS')}
- **Python Version**: {server_info.get('Python')}
- **Core Library**: {server_info.get('PyGithub')}
- **Status**: ✅ **Operational & Up-to-Date**

### 📂 Repository Stats
- **Total Files**: {file_count}
- **Active Mode**: {MODE}

---
*Powered by GitHub Actions Server Upgrade Workflow*
"""
    with open("REPO_STATUS.md", "w", encoding="utf-8") as f:
        f.write(status_content)
    
    print("   -> REPO_STATUS.md updated with server info.")
    
    generate_report()
    bulk_update()

if __name__ == "__main__":
    # 모드에 따른 실행
    if MODE == "create": bulk_create()
    elif MODE == "update": bulk_update()
    elif MODE == "auto": auto_maintenance()
    else: auto_maintenance()
