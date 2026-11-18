"""Emit a truthful training-readiness assessment without starting training."""
from pathlib import Path
import csv,json
ROOT=Path(__file__).parents[1]
def main():
    inventory=ROOT/'data/manifests/annotation_inventory.csv'; rows=list(csv.DictReader(inventory.open(encoding='utf-8')))
    approved=[r for r in rows if r.get('review_status')=='approved' and r.get('verified_class') in {'BONA_FIDE','MORPHED'}]
    cache=ROOT/'data/cache/image_features/processing_summary.json'; cache_summary=json.loads(cache.read_text()) if cache.exists() else {}
    result={'training_ready':bool(approved),'approved_bona_fide':sum(r.get('verified_class')=='BONA_FIDE' for r in approved),'approved_morphed':sum(r.get('verified_class')=='MORPHED' for r in approved),'pending_review':sum(r.get('review_status')=='pending_review' for r in rows),'cache_feature_records':cache_summary.get('feature_records',0),'blockers':[]}
    if not approved: result['blockers'].append('No explicitly approved binary labels exist; supervised training is refused.')
    result['blockers'] += ['No approved leakage-safe train/validation/test split exists.','No independent test protocol can be executed without approved labels.']
    print(json.dumps(result,indent=2)); (ROOT/'data/metadata/training_readiness.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
if __name__=='__main__': main()
