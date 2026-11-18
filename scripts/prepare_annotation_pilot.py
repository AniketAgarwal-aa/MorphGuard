"""Prepare a traceable, label-neutral evidence package for the existing review batch."""
from __future__ import annotations
import csv,json,hashlib,math
from pathlib import Path
from PIL import Image,ImageDraw
ROOT=Path(__file__).parents[1]
def digest(path):
    h=hashlib.sha256();
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024),b''): h.update(chunk)
    return h.hexdigest()
def main():
    batch=ROOT/'data/manifests/targeted_review_batch.csv'; proc=ROOT/'data/cache/image_features/processing_manifest.csv'; out=ROOT/'data/review_pilot'; out.mkdir(parents=True,exist_ok=True)
    with batch.open(newline='',encoding='utf-8') as f: rows=list(csv.DictReader(f))
    processed={}
    if proc.exists():
        with proc.open(newline='',encoding='utf-8') as f: processed={r['image_path']:r for r in csv.DictReader(f)}
    fields=['record_id','image_path','dataset','category','subject_id','morph_pair_id','source_sha256','width','height','processing_status','face_detected','face_count','brightness','contrast','sharpness','feature_shard','provenance_reference','eligibility','eligibility_reason','review_status']
    evidence=[]; missing=[]
    for i,row in enumerate(rows,1):
        rel=row['image_path']; path=ROOT/rel; p=processed.get(rel,{}); eligibility='ELIGIBLE_FOR_REVIEW'; reason='Source image and inventory metadata are present; class still requires documentary/human evidence.'
        if not path.exists(): eligibility='MISSING_SOURCE_IMAGE'; reason='Source-relative image path is unavailable.'; missing.append(rel)
        elif not row.get('dataset') or not row.get('category'): eligibility='INCONSISTENT_METADATA'; reason='Dataset/category metadata is incomplete.'
        elif row.get('proposed_interpretation') in {'acquisition_variant_candidate','gate_live_acquisition_stratum'}: eligibility='INSUFFICIENT_PROVENANCE'; reason='Available evidence describes acquisition/subset context, not a binary class.'
        rec={'record_id':f'PILOT-{i:04d}', 'image_path':rel, 'dataset':row.get('dataset',''),'category':row.get('category',''),'subject_id':row.get('subject_id',''),'morph_pair_id':row.get('morph_pair_id',''),'source_sha256':p.get('source_sha256') or (digest(path) if path.exists() else ''),'width':p.get('width',''),'height':p.get('height',''),'processing_status':p.get('status','not_processed'),'face_detected':p.get('face_detected',''),'face_count':p.get('face_count',''),'brightness':p.get('brightness',''),'contrast':p.get('contrast',''),'sharpness':p.get('sharpness',''),'feature_shard':p.get('feature_shard',''),'provenance_reference':'docs/MONOT_GROUND_TRUTH_REVIEW.md; docs/ONOT_GROUND_TRUTH_REVIEW.md','eligibility':eligibility,'eligibility_reason':reason,'review_status':'pending_review'}
        evidence.append(rec)
    with (out/'annotation_evidence.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=fields); w.writeheader(); w.writerows(evidence)
    # Contact sheets are deliberately small and label-neutral.
    for start in range(0,len(evidence),25):
        subset=evidence[start:start+25]; sheet=Image.new('RGB',(1000,1000),'white'); draw=ImageDraw.Draw(sheet)
        for j,rec in enumerate(subset):
            path=ROOT/rec['image_path']; x=(j%5)*200; y=(j//5)*200
            try:
                with Image.open(path) as im: im.convert('RGB').thumbnail((180,160)); sheet.paste(im,(x+10,y+10))
            except Exception: pass
            draw.text((x+8,y+175),rec['record_id'],fill='black'); draw.text((x+8,y+188),rec['category'][:22],fill='black')
        sheet.save(out/f'contact_sheet_{start//25+1:02d}.jpg',quality=88)
    summary={'records':len(evidence),'cache_exact_matches':sum(1 for r in evidence if r['processing_status']!='not_processed'),'eligibility_counts':{},'all_review_status':'pending_review','missing_source_images':len(missing),'batch_sha256':digest(batch),'evidence_manifest':str((out/'annotation_evidence.csv').relative_to(ROOT))}
    for r in evidence: summary['eligibility_counts'][r['eligibility']]=summary['eligibility_counts'].get(r['eligibility'],0)+1
    (out/'pilot_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))
if __name__=='__main__': main()
