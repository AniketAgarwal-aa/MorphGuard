import sys
from pathlib import Path
root = Path(__file__).parents[1]
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
if str(root / "src") not in sys.path:
    sys.path.insert(0, str(root / "src"))
