import os
import datetime

root_dir = "."
output_dir = "output_data"
html_content = """
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Linux File Share System</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f0f2f5; color: #333; padding: 20px; }
        .container { max-width: 1000px; margin: 0 auto; background: white; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); padding: 20px; }
        h1 { border-bottom: 2px solid #007bff; padding-bottom: 10px; color: #007bff; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }
        th { background-color: #f8f9fa; }
        tr:hover { background-color: #f1f1f1; }
        a { text-decoration: none; color: #333; font-weight: 500; display: block; }
        a:hover { color: #007bff; }
        .icon { margin-right: 10px; }
        .dir { color: #ffc107; }
        .file { color: #6c757d; }
        .footer { margin-top: 30px; text-align: center; color: #888; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>📂 Linux File Share System</h1>
        <p>All files in the repository are automatically indexed below.</p>
        
        <table>
            <thead>
                <tr>
                    <th>Type</th>
                    <th>File Name / Path</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody>
"""

# output_data 폴더를 순회하며 파일 목록 생성
for root, dirs, files in os.walk(output_dir):
    for file in files:
        full_path = os.path.join(root, file)
        # 윈도우 스타일 경로(\)를 웹 표준(/)으로 변환
        web_path = full_path.replace(os.sep, '/')
        
        # 아이콘 및 유형 결정
        icon = "📄"
        if file.endswith('.pdf'): icon = "📕"
        elif file.endswith('.log'): icon = "📝"
        elif file.endswith('.c'): icon = "💻"
        elif file.endswith('.exe') or '.' not in file: icon = "⚙️"
        
        html_content += f"""
        <tr>
            <td><span class="icon">{icon}</span></td>
            <td><a href="{web_path}" target="_blank">{web_path}</a></td>
            <td><a href="{web_path}" download>⬇️ Download</a></td>
        </tr>
        """

html_content += f"""
            </tbody>
        </table>
        <div class="footer">
            Last Scanned: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")} <br>
            Powered by GitHub Actions & Python Indexer
        </div>
    </div>
</body>
</html>
"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("✅ index.html generated with dynamic file list.")
