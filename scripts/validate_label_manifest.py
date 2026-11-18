import argparse, json
from pathlib import Path
from morphguard.dataset.labels import validate_label_manifest
p=argparse.ArgumentParser(); p.add_argument("manifest",type=Path); p.add_argument("--root",type=Path,default=Path(__file__).parents[1]); args=p.parse_args()
report=validate_label_manifest(args.manifest,args.root); print(json.dumps(report,indent=2)); raise SystemExit(0 if report["valid"] else 1)
