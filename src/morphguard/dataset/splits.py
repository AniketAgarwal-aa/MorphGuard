from __future__ import annotations
import csv, random
from collections import defaultdict
from pathlib import Path

def create_group_splits(manifest: Path, output: Path, seed=42, ratios=(.70,.15,.15)):
    """Group by subject identifier to prevent known identity/derivative leakage."""
    rows=list(csv.DictReader(manifest.open(encoding="utf-8")))
    groups=defaultdict(list)
    for row in rows:
        if row["valid"].lower()=="true" and row["label"] in {"genuine","morphed"}: groups[row["subject_id"]].append(row)
    ids=list(groups); random.Random(seed).shuffle(ids); n=len(ids); cut1=int(n*ratios[0]); cut2=cut1+int(n*ratios[1])
    output.mkdir(parents=True,exist_ok=True)
    for split, selected in {"train":ids[:cut1],"validation":ids[cut1:cut2],"test":ids[cut2:]}.items():
        with (output/f"{split}.csv").open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=rows[0].keys()); w.writeheader()
            for group in selected: w.writerows(groups[group])
