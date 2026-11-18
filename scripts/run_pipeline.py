"""Safe coordinator. Full processing requires explicit commands; audit is the default."""
import argparse, subprocess, sys
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument("stage",choices=["audit","splits","features","baselines"],default="audit",nargs="?");p.add_argument("--hash-duplicates",action="store_true");args=p.parse_args(); root=Path(__file__).parents[1]
cmd={"audit":[sys.executable,"scripts/audit_datasets.py"],"splits":[sys.executable,"scripts/create_splits.py","data/metadata/monot_inventory.csv"],"features":[sys.executable,"scripts/extract_features.py","data/splits/train.csv"],"baselines":[sys.executable,"scripts/train_baselines.py","data/cache/features"]}[args.stage]
if args.hash_duplicates and args.stage=="audit":cmd.append("--hash-duplicates")
raise SystemExit(subprocess.call(cmd,cwd=root))
