from __future__ import annotations
import csv, hashlib, json, random
from collections import defaultdict, Counter
from pathlib import Path
from .labels import approved_rows

def _manifest_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create_group_splits(manifest: Path, output: Path, seed=42, ratios=(.70,.15,.15), project_root: Path | None = None):
    """Create identity/pair-grouped splits only from approved reviewed rows."""
    root=project_root or Path(__file__).resolve().parents[3]
    rows=approved_rows(manifest,root)
    if not rows: raise ValueError('No approved rows available for split creation')
    groups=defaultdict(list)
    for row in rows:
        key=row.get('subject_id') or row.get('morph_pair_id') or row['image_path']
        groups[key].append(row)
    ids=list(groups); random.Random(seed).shuffle(ids); n=len(ids); cut1=int(n*ratios[0]); cut2=cut1+int(n*ratios[1])
    assignments={key:split for split, selected in {'train':ids[:cut1],'validation':ids[cut1:cut2],'test':ids[cut2:]}.items() for key in selected}
    output.mkdir(parents=True,exist_ok=True); split_rows={s:[] for s in ('train','validation','test')}
    for key,items in groups.items():
        for row in items: split_rows[assignments[key]].append(row)
    fields=list(rows[0].keys())
    for split,items in split_rows.items():
        with (output/f'{split}.csv').open('w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(items)
    identity_splits=defaultdict(set); pair_splits=defaultdict(set)
    for split,items in split_rows.items():
        for row in items:
            if row.get('subject_id'): identity_splits[row['subject_id']].add(split)
            if row.get('morph_pair_id'): pair_splits[row['morph_pair_id']].add(split)
    leakage={"identity_overlap":{k:sorted(v) for k,v in identity_splits.items() if len(v)>1},"morph_pair_overlap":{k:sorted(v) for k,v in pair_splits.items() if len(v)>1}}
    summary={"seed":seed,"ratios":ratios,"manifest":str(manifest),"manifest_sha256":_manifest_hash(manifest),"rows":{s:len(v) for s,v in split_rows.items()},"labels":{s:dict(Counter(r['verified_label'] for r in v)) for s,v in split_rows.items()},"leakage":leakage}
    (output/'split_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
    (output/'split_validation_report.json').write_text(json.dumps({"valid":not any(leakage.values()),**leakage},indent=2),encoding='utf-8')
    if any(leakage.values()): raise ValueError(f'Split leakage detected: {leakage}')
    return summary
