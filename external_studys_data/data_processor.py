import sqlite3, os, datetime, random

timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
db_path = "output_data/database/accumulated.db"

# [1] DB 누적
def accumulate_db():
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS history (id INTEGER PRIMARY KEY, ts TEXT, msg TEXT);")
    for i in range(100):
        cur.execute("INSERT INTO history (ts, msg) VALUES (?, ?)", (timestamp, f"Data Entry {i}"))
    conn.commit()
    
    # SQL 덤프 저장
    with open(f"output_data/database/snapshots/dump_{timestamp}.sql", "w") as f:
        for line in conn.iterdump(): f.write(f"{line}\n")
    conn.close()

# [2] 웹 대시보드 (index.html)
def update_web():
    file_list = []
    for root, dirs, files in os.walk("output_data"):
        for file in files:
            path = os.path.join(root, file).replace(os.sep, '/')
            stat = os.stat(os.path.join(root, file))
            file_list.append({'name': file, 'path': path, 'time': stat.st_mtime})
    
    file_list.sort(key=lambda x: x['time'], reverse=True)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'>
        <title>System Releases</title>
        <style>
            body {{ background: #111; color: #eee; font-family: sans-serif; padding: 20px; }}
            .container {{ max-width: 1000px; margin: 0 auto; }}
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ padding: 10px; border-bottom: 1px solid #333; text-align: left; }}
            th {{ background: #222; color: #4CAF50; }}
            a {{ color: #2196F3; text-decoration: none; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>📦 System Release & File Center</h1>
            <p>Latest Check: {datetime.datetime.now()}</p>
            <table><tr><th>File</th><th>Download</th></tr>
    """
    for f in file_list:
        html += f"<tr><td>{f['name']}</td><td><a href='{f['path']}' download>Download</a></td></tr>"
    html += "</table></div></body></html>"
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    accumulate_db()
    update_web()
