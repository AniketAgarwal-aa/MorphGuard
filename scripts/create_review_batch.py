"""Create a deterministic, strata-balanced pending review cohort from the inventory."""
from __future__ import annotations
import argparse,csv,hashlib,json,random
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).parents[1]
def main():
    p=argparse.ArgumentParser(); p.add_argument('--size',type=int,default=150); p.add_argument('--seed',type=int,default=20261118); p.add_argument('--output',type=Path,default=ROOT/'data/manifests/targeted_review_batch.csv'); a=p.parse_args()
    if a.size<1: raise SystemExit('--size must be positive')
    source=ROOT/'data/manifests/annotation_inventory.csv'
    with source.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f)); fields=list(rows[0])
    rows=[r for r in rows if r.get('review_status')=='pending_review']
    strata=defaultdict(list)
    for r in rows: strata[(r.get('dataset',''),r.get('category',''))].append(r)
    rng=random.Random(a.seed)
    for values in strata.values(): rng.shuffle(values)
    chosen=[]; used_subject=set(); used_pair=set(); keys=sorted(strata)
    while len(chosen)<min(a.size,len(rows)) and keys:
        progressed=False
        for key in keys:
            values=strata[key]
            while values:
                row=values.pop(); subject=row.get('subject_id',''); pair=row.get('morph_pair_id','')
                if subject and subject in used_subject: continue
                if pair and pair in used_pair: continue
                chosen.append(row); used_subject.add(subject); used_pair.add(pair); progressed=True; break
            if len(chosen)>=a.size: break
        if not progressed: break
    a.output.parent.mkdir(parents=True,exist_ok=True)
    with a.output.open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(chosen)
    digest=hashlib.sha256(a.output.read_bytes()).hexdigest()
    meta={'source_manifest':str(source.relative_to(ROOT)),'source_manifest_sha256':hashlib.sha256(source.read_bytes()).hexdigest(),'batch_path':str(a.output.relative_to(ROOT)),'batch_sha256':digest,'rows':len(chosen),'seed':a.seed,'status':'pending_review','strata':{f'{d}/{c}':sum(1 for r in chosen if r.get('dataset')==d and r.get('category')==c) for d,c in keys}}
    a.output.with_suffix('.json').write_text(json.dumps(meta,indent=2),encoding='utf-8'); print(json.dumps(meta,indent=2))
if __name__=='__main__': main()
