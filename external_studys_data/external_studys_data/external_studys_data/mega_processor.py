import os, random, datetime, shutil

root_dir = "File_Server_Root"
data_dir = f"{root_dir}/Data"

# [1] 대용량 파일 생성 (Heavy Files)
print(">> Generating MB-Scale Files...")
# 10MB ~ 50MB 파일 5개 생성 (매번)
for i in range(5):
    size_mb = random.randint(10, 50) 
    fname = f"backup_part_{i}_{datetime.datetime.now().strftime('%H%M%S')}.dat"
    fpath = f"{data_dir}/{fname}"
    
    # 더미 데이터 쓰기 (0으로 채움)
    with open(fpath, "wb") as f:
        f.seek((size_mb * 1024 * 1024) - 1)
        f.write(b'\0')
    
    print(f" + Generated {fname} ({size_mb} MB)")

# [2] 디스크 사용량 분석
total, used, free = shutil.disk_usage("/")
used_percent = (used / total) * 100

# [3] 웹 대시보드 생성 (게이지 바 포함)
def generate_dashboard():
    files_html = ""
    # 최신 파일 20개만 표시
    all_files = []
    for r, d, f in os.walk(root_dir):
        for file in f:
            all_files.append(os.path.join(r, file))
    
    all_files.sort(key=os.path.getmtime, reverse=True)
    
    for fpath in all_files[:30]:
        fname = os.path.basename(fpath)
        size = os.path.getsize(fpath)
        size_str = f"{size/1024/1024:.2f} MB" if size > 1024*1024 else f"{size/1024:.2f} KB"
        path_display = fpath.replace("File_Server_Root", "")
        
        icon = "📄"
        if fname.endswith(".log"): icon = "📜"
        if fname.endswith(".dat"): icon = "💾"
        
        files_html += f"""
        <tr>
            <td>{icon} {fname}</td>
            <td>{path_display}</td>
            <td><b>{size_str}</b></td>
            <td><a href='{fpath}' download>⬇️ Load</a></td>
        </tr>
        """

    html = f"""
    <!DOCTYPE html>
    <html lang='ko'>
    <head>
        <meta charset='utf-8'>
        <title>Mega Server V9</title>
        <style>
            body {{ background: #000; color: #0f0; font-family: 'Courier New', monospace; padding: 20px; }}
            .container {{ max-width: 1200px; margin: 0 auto; border: 2px solid #0f0; padding: 20px; box-shadow: 0 0 20px #0f0; }}
            h1 {{ text-align: center; border-bottom: 2px solid #0f0; }}
            
            /* Disk Usage Bar */
            .disk-box {{ margin: 20px 0; border: 1px solid #333; padding: 10px; background: #111; }}
            .progress-bg {{ background: #333; height: 25px; width: 100%; border-radius: 5px; overflow: hidden; }}
            .progress-bar {{ background: linear-gradient(90deg, #0f0, #ff0); height: 100%; width: {used_percent}%; transition: width 0.5s; }}
            
            table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
            th, td {{ border: 1px solid #0f0; padding: 10px; text-align: left; }}
            th {{ background: #002200; }}
            a {{ color: #0ff; text-decoration: none; }}
            
            .boot-log {{ background: #111; color: #aaa; padding: 10px; border: 1px solid #444; height: 150px; overflow-y: scroll; font-size: 0.9em; }}
        </style>
    </head>
    <body>
        <div class='container'>
            <h1>🖥️ MEGA SERVER STATUS: ONLINE</h1>
            
            <div class='disk-box'>
                <h3>💾 Disk Usage (Expanded Capacity)</h3>
                <div class='progress-bg'>
                    <div class='progress-bar'></div>
                </div>
                <p>{used // (1024**3)} GB Used / {total // (1024**3)} GB Total ({used_percent:.1f}%)</p>
            </div>

            <div class='disk-box'>
                <h3>⚡ Last Reboot Sequence</h3>
                <div class='boot-log'>
                    SYSTEM REBOOT INITIATED...<br>
                    Stopping Services... [OK]<br>
                    Unmounting... [OK]<br>
                    Booting Kernel... [OK]<br>
                    Filesystem Check... [PASSED]<br>
                    Services Started... [OK]<br>
                    System Ready at {datetime.datetime.now()}
                </div>
            </div>

            <h3>📂 Active Files (Top 30 Recent)</h3>
            <table>
                <tr><th>File</th><th>Path</th><th>Size</th><th>Action</th></tr>
                {files_html}
            </table>
        </div>
    </body>
    </html>
    """
    
    with open("index.html", "w", encoding="utf-8") as f: f.write(html)

if __name__ == "__main__":
    generate_dashboard()
