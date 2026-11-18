"""Validate existing audit metadata and annotation inventory without rescanning images."""
from pathlib import Path
import csv, json

ROOT=Path(__file__).parents[1]
EXPECTED={('MONOT','Gate_10'):2550,('MONOT','Gate_25'):6350,('MONOT','Morphed'):15240,('ONOT','digital'):11326,('ONOT','print-scan'):11326}
def main():
    summary=json.loads((ROOT/'data/metadata/annotation_audit_summary.json').read_text(encoding='utf-8'))
    assert summary['records']==46792 and summary['approved_for_training']==0
    with (ROOT/'data/manifests/annotation_inventory.csv').open(encoding='utf-8') as f: rows=list(csv.DictReader(f))
    assert len(rows)==46792
    observed={}
    for row in rows: observed[(row['dataset'],row['category'])]=observed.get((row['dataset'],row['category']),0)+1
    assert observed==EXPECTED
    categories={f'{dataset}/{category}': count for (dataset,category), count in observed.items()}
    print(json.dumps({'valid':True,'records':len(rows),'approved_for_training':summary['approved_for_training'],'categories':categories},indent=2))
if __name__=='__main__': main()
