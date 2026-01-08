import os
import sys
import random
import csv
from datetime import datetime
from github import Github

# --- 환경 변수 로드 ---
TOKEN = os.getenv('GH_TOKEN')
REPO_NAME = os.getenv('REPO_NAME')
MODE = os.getenv('MODE')
COUNT = int(os.getenv('COUNT', 5))

if not TOKEN or not REPO_NAME:
    print("Error: GH_TOKEN or REPO_NAME is missing.")
    sys.exit(1)

g = Github(TOKEN)
repo = g.get_repo(REPO_NAME)

print(f"🚀 Started Issue Manager")
print(f"Target Repo: {REPO_NAME}")
print(f"Mode: {MODE} | Count Limit: {COUNT}")

def bulk_create():
    """테스트용 이슈 대량 생성"""
    print(">> [Mode] Bulk Create")
    prefixes = ["[Bug]", "[Feature]", "[Docs]", "[Refactor]", "[Question]"]
    for i in range(COUNT):
        title = f"{random.choice(prefixes)} 자동 생성된 이슈 #{random.randint(1000, 9999)}"
        body = f"이 이슈는 Python 스크립트에 의해 자동 생성되었습니다.\n생성 시간: {datetime.now()}"
        issue = repo.create_issue(title=title, body=body)
        print(f"✅ Created #{issue.number}: {title}")

def bulk_update():
    """기존 이슈 대량 분석 및 라벨링 (Mock AI)"""
    print(">> [Mode] Bulk Update & Label")
    issues = repo.get_issues(state='open')
    processed = 0
    
    for issue in issues:
        if processed >= COUNT: break
        
        labels = []
        if "Bug" in issue.title or "오류" in issue.title:
            labels.append("bug")
        elif "Feature" in issue.title or "기능" in issue.title:
            labels.append("enhancement")
        
        if labels:
            # 기존 라벨과 합치기
            current_labels = [l.name for l in issue.labels]
            new_labels = [l for l in labels if l not in current_labels]
            if new_labels:
                issue.add_to_labels(*new_labels)
                issue.create_comment(f"🤖 **Auto-Bot**: 라벨 {new_labels}이(가) 추가되었습니다.")
                print(f"🔧 Updated #{issue.number}: Added {new_labels}")
        
        processed += 1

def bulk_close():
    """오래된 이슈 대량 닫기 (예: 'wontfix' 라벨이 있거나 제목에 'Close'가 있는 경우)"""
    print(">> [Mode] Bulk Close")
    issues = repo.get_issues(state='open')
    processed = 0
    
    for issue in issues:
        if processed >= COUNT: break
        
        # 예시 조건: 제목에 'test'나 '임시'가 들어가면 닫음
        if "test" in issue.title.lower() or "임시" in issue.title:
            issue.create_comment("🤖 **Auto-Bot**: 정리 정책에 따라 이슈를 자동으로 닫습니다.")
            issue.edit(state='closed')
            print(f"zzz Closed #{issue.number}: {issue.title}")
            processed += 1

def generate_report():
    """모든 이슈를 스캔하여 CSV 리포트 생성 (서버 업로드용 파일 생성)"""
    print(">> [Mode] Generate Report")
    issues = repo.get_issues(state='all')
    filename = "issue_report.csv"
    
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(["Number", "Title", "State", "Labels", "Created At"])
        
        limit_cnt = 0
        for issue in issues:
            if limit_cnt >= COUNT * 10: break # 리포트는 더 많이 스캔
            labels = ", ".join([l.name for l in issue.labels])
            writer.writerow([issue.number, issue.title, issue.state, labels, issue.created_at])
            limit_cnt += 1
            
    print(f"📄 Report generated: {filename}")

# --- 메인 실행 분기 ---
if __name__ == "__main__":
    if MODE == "create":
        bulk_create()
    elif MODE == "update":
        bulk_update()
    elif MODE == "close":
        bulk_close()
    elif MODE == "report":
        generate_report()
    elif MODE == "all":
        # 모든 기능 순차 실행
        bulk_create()
        bulk_update()
        generate_report()
    else:
        print(f"Unknown Mode: {MODE}")
