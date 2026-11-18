import re
from pathlib import Path

secret_patterns = [
    re.compile(r'(api[_-]?key|secret|password|bearer|token)\s*[:=]\s*["\'][a-zA-Z0-9_\-]{16,}["\']', re.IGNORECASE),
    re.compile(r'ghp_[A-Za-z0-9]{36}'),
    re.compile(r'sk-[A-Za-z0-9]{32,}'),
    re.compile(r'AKIA[0-9A-Z]{16}'),
]

root = Path('.')
suspects = []

for p in ['.gitignore', 'README.md', 'FINAL_REPORT.md', 'ARCHITECTURE.md', 'DEMONSTRATION_GUIDE.md', 'PROJECT_OVERVIEW.md', '.streamlit', 'app', 'docs', 'models/metadata', 'data/metadata', 'scripts', 'src', 'tests']:
    path_obj = root / p
    files = [path_obj] if path_obj.is_file() else list(path_obj.rglob('*'))
    for f in files:
        if f.is_file() and f.suffix in ('.py', '.md', '.json', '.toml', '.yaml', '.yml'):
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')
                for pat in secret_patterns:
                    for m in pat.finditer(content):
                        suspects.append((str(f), m.group(0)[:60]))
            except Exception:
                pass

print(f"Secret scan complete. Matches: {len(suspects)}")
for s in suspects:
    print(" ", s)
