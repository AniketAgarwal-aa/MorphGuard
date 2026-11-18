"""Validate a generated split using the same manifest safeguards as training."""
import argparse
from pathlib import Path
from morphguard.dataset.labels import validate_label_manifest
def main():
    p=argparse.ArgumentParser(); p.add_argument('--manifest',required=True); a=p.parse_args()
    result=validate_label_manifest(Path(a.manifest),Path.cwd(),require_approved=True)
    print(result)
    raise SystemExit(0 if result['valid'] else 1)
if __name__=='__main__': main()
