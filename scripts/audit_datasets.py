"""Stream raw MONOT and ONOT inventories; never writes into either dataset."""
import argparse
from pathlib import Path
from morphguard.dataset import audit

p=argparse.ArgumentParser(); p.add_argument("--root",type=Path,default=Path(__file__).parents[1]); p.add_argument("--hash-duplicates",action="store_true"); p.add_argument("--batch-size",type=int,default=100); p.add_argument("--sample-limit",type=int); p.add_argument("--dataset",choices=["MONOT","ONOT"],action="append"); p.add_argument("--resume",action="store_true",help="accepted for CLI compatibility; generated CSVs are atomically replaceable"); p.add_argument("--force-rescan",action="store_true")
args=p.parse_args(); selected=tuple(args.dataset) if args.dataset else ("MONOT","ONOT"); print(audit(args.root,args.root/"data"/"metadata",args.hash_duplicates,args.sample_limit,selected,args.batch_size))
