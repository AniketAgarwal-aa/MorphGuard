"""Report annotation coverage without approving any sample."""
import argparse,csv,json
from pathlib import Path
from collections import Counter
p=argparse.ArgumentParser(); p.add_argument('--manifest',type=Path,default=Path('data/manifests/label_manifest.csv')); p.add_argument('--output',type=Path,default=Path('data/metadata/label_review_summary.json')); args=p.parse_args()
if not args.manifest.exists():
    report={'manifest_present':False,'rows':0,'approved':0,'status_counts':{},'message':'No reviewed manifest exists; all audited records remain unreviewed.'}
else:
    with args.manifest.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    statuses=Counter(r.get('reviewer_status','') for r in rows); report={'manifest_present':True,'rows':len(rows),'approved':sum(r.get('reviewer_status')=='approved' for r in rows),'status_counts':dict(statuses)}
args.output.parent.mkdir(parents=True,exist_ok=True); args.output.write_text(json.dumps(report,indent=2),encoding='utf-8'); print(json.dumps(report,indent=2))
