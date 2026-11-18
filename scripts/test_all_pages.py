"""Verify all 14 Streamlit pages run without exceptions."""
import sys, os
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / 'src'))
sys.path.insert(0, str(ROOT))

from streamlit.testing.v1 import AppTest

pages = [
    'app/pages/overview.py',
    'app/pages/1_Face_Morph_Analysis.py',
    'app/pages/4_Dataset_Explorer.py',
    'app/pages/annotation_review.py',
    'app/pages/2_Model_Comparison.py',
    'app/pages/3_Explainability.py',
    'app/pages/5_Research_Experiments.py',
    'app/pages/about.py',
    'app/pages/how_it_works.py',
    'app/pages/datasets.py',
    'app/pages/models_technology.py',
    'app/pages/6_Methodology.py',
    'app/pages/7_Limitations_And_Info.py',
    'app/pages/technical_documentation.py',
]

results = []
all_passed = True

print(f"Testing {len(pages)} Streamlit pages...\n")
for p in pages:
    page_path = ROOT / p
    name = page_path.name
    try:
        at = AppTest.from_file(str(page_path), default_timeout=30)
        at.run()
        has_error = bool(at.exception)
        exc_info = str(at.exception[0].value) if at.exception else None
        
        status = "FAIL" if has_error else "PASS"
        if has_error:
            all_passed = False
            print(f"  ❌ {name:<32} -> {status}: {exc_info}")
        else:
            print(f"  ✓ {name:<32} -> {status}")
        results.append({'page': name, 'status': status, 'error': exc_info})
    except Exception as exc:
        all_passed = False
        print(f"  ❌ {name:<32} -> CRASH: {exc}")
        results.append({'page': name, 'status': 'CRASH', 'error': str(exc)})

print(f"\nSummary: {sum(1 for r in results if r['status'] == 'PASS')} / {len(pages)} pages passed.")
sys.exit(0 if all_passed else 1)
