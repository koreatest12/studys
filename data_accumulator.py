import sqlite3, os, datetime, random

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
db_path = "output_data/database/accumulated.db"

# [1] DB 데이터 누적 (Append Data)
def accumulate_db_data():
    print(f">> Accumulating Data into {db_path}...")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    
    # 테이블 생성 (존재하면 건너뜀)
    cur.execute("CREATE TABLE IF NOT EXISTS access_history (id INTEGER PRIMARY KEY, timestamp TEXT, user TEXT, action TEXT, ip TEXT);")
    
    # 데이터 추가 (기존 데이터 보존 + 500건 추가)
    users = ['User_A', 'User_B', 'Admin', 'System', 'Guest']
    actions = ['LOGIN', 'DOWNLOAD', 'UPLOAD', 'SYNC_ERROR', 'CHECK_STATUS']
    
    for _ in range(500):
        cur.execute("INSERT INTO access_history (timestamp, user, action, ip) VALUES (?, ?, ?, ?)", 
                    (datetime.datetime.now(), random.choice(users), random.choice(actions), f"192.168.1.{random.randint(1,255)}"))
    
    conn.commit()
    
    # 현재 상태 스냅샷 저장 (SQL 파일 누적)
    dump_file = f"output_data/database/snapshots/db_dump_{timestamp}.sql"
    with open(dump_file, "w") as f:
        for line in conn.iterdump(): f.write(f"{line}\n")
    
    conn.close()

# [2] 웹 대시보드 갱신 (누적된 파일 리스트업)
def update_dashboard():
    print(">> Updating Web Dashboard with History...")
    
    file_list = []
    for root, dirs, files in os.walk("output_data"):
        for file in files:
            path = os.path.join(root, file).replace(os.sep, '/')
            stat = os.stat(os.path.join(root, file))
            mod_time = datetime.datetime.fromtimestamp(stat.st_mtime)
            file_list.append({'name': file, 'path': path, 'time': mod_time})
    
    # 최신순 정렬
    file_list.sort(key=lambda x: x['time'], reverse=True)
    
    html = f"""
    <!DOCTYPE html>
    <html lang='ko'>
    <head>
        <meta charset='utf-8'>
        <title>Accumulated Data Center</title>
        <style>
            body {{ background: #121212; color: #e0e0e0; font-family: 'Segoe UI', sans-serif; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; }}
            h1 {{ border-bottom: 3px solid #03dac6; padding-bottom: 10px; color: #03dac6; }}
            .stats {{ background: #1e1e1e; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
            .table-wrapper {{ max-height: 800px; overflow-y: auto; background: #1e1e1e; border-radius: 8px; border: 1px solid #333; }}
            table {{ width: 100%; border-collapse: collapse; }}
            th {{ position: sticky; top: 0; background: #333; color: #03dac6; padding: 12px; text-align: left; z-index: 10; }}
            td {{ padding: 10px; border-bottom: 1px solid #2c2c2c; }}
            tr:hover {{ background: #2c2c2c; }}
            a {{ color: #81d4fa; text-decoration: none; }}
            .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; color: black; }}
            .sql {{ background: #ffca28; }}
            .log {{ background: #a5d6a7; }}
            .db {{ background: #ef5350; color: white; }}
            .c {{ background: #90caf9; color: black; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>🚀 Concurrent & Accumulated Data Center</h1>
            <div class='stats'>
                <strong>Total Files:</strong> {len(file_list)} <br>
                <strong>Last Update:</strong> {datetime.datetime.now()} <br>
                <strong>Status:</strong> Active & Accumulating
            </div>
            <div class='table-wrapper'>
                <table>
                    <thead><tr><th>Time</th><th>Type</th><th>File Name</th><th>Download</th></tr></thead>
                    <tbody>
    """
    
    for f in file_list:
        ext = f['name'].split('.')[-1]
        badge_class = "badge"
        if ext == 'sql': badge_class += " sql"
        elif ext == 'log': badge_class += " log"
        elif ext == 'db': badge_class += " db"
        elif ext == 'c': badge_class += " c"
        
        html += f"""
        <tr>
            <td>{f['time'].strftime('%Y-%m-%d %H:%M:%S')}</td>
            <td><span class='{badge_class}'>{ext.upper()}</span></td>
            <td>{f['name']}</td>
            <td><a href='{f['path']}' download>⬇️ Load</a></td>
        </tr>
        """
        
    html += "</tbody></table></div></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

if __name__ == "__main__":
    accumulate_db_data()
    update_dashboard()
