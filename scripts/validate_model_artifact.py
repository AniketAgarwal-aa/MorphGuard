import argparse, json
from pathlib import Path
from morphguard.inference.artifacts import validate_artifact
p=argparse.ArgumentParser(); p.add_argument('model',type=Path); p.add_argument('metadata',type=Path); args=p.parse_args(); report=validate_artifact(args.model,args.metadata); print(json.dumps(report,indent=2)); raise SystemExit(0 if report['valid'] else 1)
