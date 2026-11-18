"""Validate image-processing manifest and feature shards."""
from pathlib import Path
import csv,json,numpy as np
ROOT=Path(__file__).parents[1]
def main():
    cache=ROOT/'data/cache/image_features'; manifest=cache/'processing_manifest.csv'; summary=json.loads((cache/'processing_summary.json').read_text())
    with manifest.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    shards=list(cache.glob('features_*.npz')); feature_rows=0; dims=set()
    for path in shards:
        with np.load(path) as z:
            n=len(z['paths']); feature_rows+=n; dims.add((z['X'].shape[1],z['lbp'].shape[1],z['hog'].shape[1],z['glcm'].shape[1])); assert np.isfinite(z['X']).all()
    result={'valid':len(rows)==summary['requested'] and feature_rows==summary['feature_records'] and len(dims)==1,'manifest_rows':len(rows),'feature_rows':feature_rows,'feature_dimensions':sorted(dims)}
    print(json.dumps(result,indent=2)); raise SystemExit(0 if result['valid'] else 1)
if __name__=='__main__': main()
