import subprocess, time, pathlib, sys

profile_dir = pathlib.Path('C:/Users/admin/AppData/Local/Temp/chrome_test_profile')
profile_dir.mkdir(parents=True, exist_ok=True)
chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
cmd = [
    chrome_path,
    '--remote-debugging-port=9222',
    f'--user-data-dir={profile_dir}',
    '--headless=new',
    '--disable-gpu',
    'http://127.0.0.1:8501'
]
proc = subprocess.Popen(cmd)
print(f"Chrome running with PID {proc.pid}", flush=True)
try:
    proc.wait()
except KeyboardInterrupt:
    proc.terminate()
