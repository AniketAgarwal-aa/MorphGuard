"""Build a provenance-first annotation inventory from MONOT/ONOT files.

This script records evidence and proposed interpretations only. It never approves
labels and never reads image pixels, so it is safe to rerun without a raw audit.
"""
from __future__ import annotations
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

ROOT=Path(__file__).parents[1]; META=ROOT/'data'/'metadata'; OUT=ROOT/'data'/'manifests'/'annotation_inventory.csv'
IMAGE_EXT={'.png','.jpg','.jpeg','.bmp','.tif','.tiff','.webp'}
SUBJECT_RE=re.compile(r'(?P<id>S\d{5,})')
MORPH_RE=re.compile(r'^M_(S\d+-.+?)_(S\d+-.+?)_(C\d+)_B(\d+)_W(\d+)_PA(\d+)_PM(\d+)_F00',re.I)

def threshold_membership():
    membership=defaultdict(list)
    for path in sorted((ROOT/'ONOT').glob('threshold=*_cosine_images.txt')):
        threshold=re.search(r'threshold=([^_]+)',path.name)
        value=threshold.group(1) if threshold else 'unknown'
        for line in path.read_text(encoding='utf-8',errors='replace').splitlines():
            tokens=line.split()
            if not tokens: continue
            # Official format places the ICAO-compliant image first on each line.
            candidate=tokens[0].replace('\\','/')
            if Path(candidate).suffix.lower() in IMAGE_EXT:
                membership[Path(candidate).name].append(value)
    return membership

def main():
    thresholds=threshold_membership(); fields=['image_path','dataset','category','original_annotation','proposed_interpretation','label_provenance','subject_id','morph_pair_id','review_status','inclusion_status','reason','threshold_membership']
    counts=Counter(); subjects=Counter(); pairs=Counter(); statuses=Counter(); provenance=Counter(); rows=[]
    for manifest in (META/'monot_inventory.csv',META/'onot_inventory.csv'):
        with manifest.open(encoding='utf-8',newline='') as f:
            for record in csv.DictReader(f):
                path=record['path']; parts=Path(path).parts; dataset=record['dataset']; category=record['category']; name=Path(path).name
                subject=''; pair=''; interpretation='unknown'; source='none'; reason='No image-level reviewed ground truth present'; threshold=','.join(thresholds.get(name,[]))
                match=SUBJECT_RE.search(name)
                if dataset=='ONOT':
                    subject=parts[2] if len(parts)>2 and parts[2].startswith('S') else (match.group('id') if match else '')
                    interpretation='acquisition_variant_candidate'; source='ONOT folder + filename convention; threshold membership is subset evidence only'
                    reason='Acquisition variant is observable; genuine/morphed status is not an image-level label in local files'
                    if threshold: source+='; threshold annotation file'
                elif category=='Morphed':
                    morph=MORPH_RE.match(name)
                    ids=SUBJECT_RE.findall(name); subject=ids[0] if ids else ''; pair='|'.join(ids[:2]) if len(ids)>=2 else ''
                    interpretation='morphed_attack_candidate'; source='MONOT filename encodes two source identities, algorithm and morph parameters'; reason='Strong generation evidence, but still pending reviewed protocol inclusion'
                else:
                    subject=match.group('id') if match else ''
                    interpretation='gate_live_acquisition_stratum'; source='MONOT gate category + filename convention'; reason='Gate image is a live-acquisition simulation, not an automatic attack or bona-fide class'
                row={'image_path':path,'dataset':dataset,'category':category,'original_annotation':category,'proposed_interpretation':interpretation,'label_provenance':source,'subject_id':subject,'morph_pair_id':pair,'review_status':'pending_review','inclusion_status':'not_approved','reason':reason,'threshold_membership':threshold}
                rows.append(row); counts[(dataset,category,interpretation)]+=1; statuses[row['review_status']]+=1; provenance[dataset]+=1
                if subject: subjects[(dataset,subject)]+=1
                if pair: pairs[pair]+=1
    OUT.parent.mkdir(parents=True,exist_ok=True)
    with OUT.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
    summary={'records':len(rows),'official_annotation_files':sorted(p.name for p in (ROOT/'ONOT').glob('threshold=*_cosine_images.txt')),'non_image_annotation_files':sorted(str(p.relative_to(ROOT)) for p in list((ROOT/'MONOT').rglob('*'))+list((ROOT/'ONOT').rglob('*')) if p.is_file() and p.suffix.lower() not in IMAGE_EXT and p.name.lower()!='thumbs.db'),'status_counts':dict(statuses),'proposed_interpretations':{('|'.join(k)):v for k,v in counts.items()},'records_with_subject_id':sum(1 for r in rows if r['subject_id']),'records_with_morph_pair_id':sum(1 for r in rows if r['morph_pair_id']),'records_with_threshold_membership':sum(1 for r in rows if r['threshold_membership']),'approved_for_training':0,'review_required':len(rows),'notes':['No raw CSV/Excel/JSON/XML image-level ground-truth manifest was found.','Interpretations are provenance records only and are not approved labels.','MONOT Morphed filenames expose source-pair and algorithm parameters; MONOT gate filenames expose source subject IDs.','ONOT subject folders expose subject IDs; threshold files describe subset membership.']}
    (META/'annotation_audit_summary.json').write_text(json.dumps(summary,indent=2),encoding='utf-8'); print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
