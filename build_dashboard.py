import os, datetime

root_dir = "File_Server_Root"
total_files = 0
total_size = 0
file_rows = ""

# 파일 탐색 및 HTML 행 생성
for root, dirs, files in os.walk(root_dir):
    for file in files:
        total_files += 1
        path = os.path.join(root, file)
        size = os.path.getsize(path)
        total_size += size
        
        # 웹 경로 변환
        web_path = path.replace(os.sep, '/')
        parent_dir = os.path.basename(root)
        
        # 아이콘 결정
        ext = file.split('.')[-1]
        icon = "📄"
        badge_color = "#6c757d"
        if ext in ['conf', 'xml', 'json']: icon, badge_color = "⚙️", "#ff9800" # Config
        elif ext in ['log']: icon, badge_color = "📝", "#4caf50" # Log
        elif ext in ['sql']: icon, badge_color = "🗄️", "#2196f3" # DB
        elif ext in ['py', 'java', 'c']: icon, badge_color = "💻", "#9c27b0" # Code
        elif 'vmlinuz' in file: icon, badge_color = "🐧", "#E91E63" # Kernel

        file_rows += f"""
        <tr class="file-row">
            <td><span class="icon">{icon}</span> {file}</td>
            <td><span class="badge" style="background:{badge_color}">{parent_dir}</span></td>
            <td>{size} B</td>
            <td>{datetime.datetime.now().strftime('%H:%M:%S')}</td>
            <td><a href="{web_path}" download class="btn-download">⬇️ Load</a></td>
        </tr>
        """

# HTML 템플릿 (Glassmorphism Dark Theme)
html = f"""
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Enterprise Cloud Server</title>
    <style>
        :root {{ --bg: #0f172a; --card: #1e293b; --text: #f1f5f9; --accent: #38bdf8; }}
        body {{ font-family: 'Segoe UI', sans-serif; background: var(--bg); color: var(--text); margin: 0; padding: 20px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        /* Header & Stats */
        header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; padding: 20px; background: var(--card); border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        h1 {{ margin: 0; background: linear-gradient(45deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .stats {{ display: flex; gap: 20px; }}
        .stat-box {{ text-align: center; }}
        .stat-val {{ font-size: 1.5em; font-weight: bold; color: var(--accent); }}
        
        /* Search */
        .search-bar {{ width: 100%; padding: 15px; background: var(--card); border: 1px solid #334155; color: white; border-radius: 8px; margin-bottom: 20px; font-size: 1.1em; }}
        
        /* File Table */
        .table-container {{ background: var(--card); border-radius: 12px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ background: #334155; padding: 15px; text-align: left; color: #94a3b8; font-weight: 600; }}
        td {{ padding: 12px 15px; border-bottom: 1px solid #334155; }}
        tr:hover {{ background: #334155; }}
        
        /* Components */
        .badge {{ padding: 4px 8px; border-radius: 4px; font-size: 0.8em; font-weight: bold; color: white; }}
        .btn-download {{ padding: 6px 12px; background: var(--accent); color: #0f172a; text-decoration: none; border-radius: 6px; font-weight: bold; transition: 0.2s; }}
        .btn-download:hover {{ opacity: 0.8; }}
        .icon {{ margin-right: 8px; }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div>
                <h1>☁️ Enterprise Cloud Server V8</h1>
                <small>Managed by GitHub Actions • Branch: main</small>
            </div>
            <div class="stats">
                <div class="stat-box"><div class="stat-val">{total_files}</div><div>Files</div></div>
                <div class="stat-box"><div class="stat-val">{total_size / 1024:.1f} KB</div><div>Size</div></div>
                <div class="stat-box"><div class="stat-val">Online</div><div>Status</div></div>
            </div>
        </header>

        <input type="text" id="search" class="search-bar" placeholder="🔍 Search files, config, logs..." onkeyup="filterFiles()">

        <div class="table-container">
            <table id="fileTable">
                <thead><tr><th>File Name</th><th>Directory</th><th>Size</th><th>Time</th><th>Action</th></tr></thead>
                <tbody>
                    {file_rows}
                </tbody>
            </table>
        </div>
    </div>

    <script>
        function filterFiles() {{
            const input = document.getElementById('search');
            const filter = input.value.toUpperCase();
            const table = document.getElementById('fileTable');
            const tr = table.getElementsByTagName('tr');
            for (let i = 0; i < tr.length; i++) {{
                const td = tr[i].getElementsByTagName('td')[0];
                if (td) {{
                    const txt = td.textContent || td.innerText;
                    tr[i].style.display = txt.toUpperCase().indexOf(filter) > -1 ? "" : "none";
                }}
            }}
        }}
    </script>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f: f.write(html)
print("✅ Enterprise Dashboard Generated.")
