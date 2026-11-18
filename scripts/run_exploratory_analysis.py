"""Produce descriptive, label-free analysis from existing audit metadata only."""
from __future__ import annotations
import csv,json,statistics
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).parents[1]
def main():
    files=[ROOT/'data/metadata/monot_inventory.csv',ROOT/'data/metadata/onot_inventory.csv']; rows=[]
    for path in files:
        with path.open(newline='',encoding='utf-8') as f: rows.extend(csv.DictReader(f))
    def nums(key):
        vals=[float(r[key]) for r in rows if r.get(key) not in ('',None)]
        return {'count':len(vals),'min':min(vals) if vals else None,'median':statistics.median(vals) if vals else None,'max':max(vals) if vals else None}
    annotation=[]
    with (ROOT/'data/manifests/annotation_inventory.csv').open(newline='',encoding='utf-8') as f: annotation=list(csv.DictReader(f))
    subjects=Counter(r.get('subject_id','') for r in annotation if r.get('subject_id')); pairs=Counter(r.get('morph_pair_id','') for r in annotation if r.get('morph_pair_id'))
    out={'records':len(rows),'dimensions':nums('width'),'heights':nums('height'),'file_sizes':nums('file_size'),'by_dataset':dict(Counter(r.get('dataset') for r in rows)),'by_category':dict(Counter(f"{r.get('dataset')}/{r.get('category')}" for r in rows)),'subject_group_sizes':{'groups':len(subjects),'max':max(subjects.values()) if subjects else 0,'median':statistics.median(subjects.values()) if subjects else 0},'candidate_pair_group_sizes':{'groups':len(pairs),'max':max(pairs.values()) if pairs else 0,'median':statistics.median(pairs.values()) if pairs else 0},'interpretation':'Descriptive metadata only; no cluster or anomaly output is a morph/genuine label.'}
    path=ROOT/'data/metadata/exploratory_analysis.json'; path.write_text(json.dumps(out,indent=2),encoding='utf-8'); print(json.dumps(out,indent=2))
if __name__=='__main__': main()
