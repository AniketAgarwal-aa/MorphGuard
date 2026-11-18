import argparse
from pathlib import Path
from morphguard.dataset import create_group_splits
p=argparse.ArgumentParser(); p.add_argument("manifest",type=Path); p.add_argument("--output",type=Path,default=Path("data/splits")); args=p.parse_args()
create_group_splits(args.manifest,args.output)
