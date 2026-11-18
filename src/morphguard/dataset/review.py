"""Safe, auditable operations for the human annotation manifest."""
from __future__ import annotations
import csv, json, os, shutil, tempfile, hashlib
from datetime import datetime, timezone
from pathlib import Path

STATUS = {'pending_review','approved','rejected','insufficient_evidence'}
CLASSES = {'BONA_FIDE','MORPHED','UNKNOWN'}
REQUIRED_APPROVAL = ('verified_class','evidence_source','review_notes','identity_verified')

def read_manifest(path: Path) -> tuple[list[dict], list[str]]:
    with path.open(newline='', encoding='utf-8') as f:
        reader=csv.DictReader(f); return list(reader), list(reader.fieldnames or [])

def review_summary(path: Path) -> dict:
    rows,_=read_manifest(path); by_dataset={}; by_category={}; statuses={}
    for row in rows:
        status=row.get('review_status','pending_review'); statuses[status]=statuses.get(status,0)+1
        key=row.get('dataset','unknown'); by_dataset.setdefault(key,{}); by_dataset[key][status]=by_dataset[key].get(status,0)+1
        key=row.get('category','unknown'); by_category.setdefault(key,{}); by_category[key][status]=by_category[key].get(status,0)+1
    return {'records':len(rows),'statuses':statuses,'by_dataset':by_dataset,'by_category':by_category,'approved_for_training':sum(1 for r in rows if r.get('review_status')=='approved' and r.get('verified_class') in {'BONA_FIDE','MORPHED'})}

def apply_review(path: Path, image_path: str, decision: dict, reviewer: str) -> dict:
    rows,fields=read_manifest(path)
    if 'record_id' not in fields: fields=['record_id']+fields
    for extra in ('verified_class','evidence_source','reviewer','review_timestamp','identity_verified','pair_verified','review_notes','review_history'):
        if extra not in fields: fields.append(extra)
    target=None
    for row in rows:
        if row.get('image_path')==image_path: target=row; break
    if target is None: raise ValueError('image_path not found in annotation manifest')
    if not reviewer or not reviewer.strip(): raise ValueError('reviewer identity is required')
    status=str(decision.get('review_status','')).lower(); verified=str(decision.get('verified_class','UNKNOWN')).upper()
    if status not in STATUS: raise ValueError(f'invalid review_status: {status}')
    if verified not in CLASSES: raise ValueError(f'invalid verified_class: {verified}')
    if status=='approved':
        if str(decision.get('eligibility','')).upper() in {'INSUFFICIENT_PROVENANCE','MISSING_SOURCE_IMAGE','INCONSISTENT_METADATA','UNKNOWN'}: raise ValueError('record is not eligible for binary approval under its provenance assessment')
        for key in REQUIRED_APPROVAL:
            if not str(decision.get(key,'')).strip(): raise ValueError(f'approved review requires {key}')
        if verified=='UNKNOWN': raise ValueError('UNKNOWN cannot be approved')
        if str(decision.get('identity_verified','')).lower() not in {'true','yes','1'}: raise ValueError('approved review requires identity_verified=true')
    if target.get('review_status')=='approved' and (status!='approved' or verified!=target.get('verified_class','')):
        raise ValueError('approved records are immutable; create a documented correction workflow instead of overwriting')
    old={k:target.get(k,'') for k in ('review_status','verified_class','reviewer','review_timestamp')}
    target.update({k:str(v) for k,v in decision.items() if k in fields})
    target['review_status']=status; target['verified_class']=verified; target['reviewer']=reviewer.strip()
    if 'verified_label' in fields: target['verified_label'] = {'BONA_FIDE':'genuine','MORPHED':'morphed','UNKNOWN':''}[verified]
    target['review_timestamp']=datetime.now(timezone.utc).isoformat()
    target['review_history']=json.dumps([old, {'review_status':status,'verified_class':verified,'reviewer':reviewer}], separators=(',',':'))
    path.parent.mkdir(parents=True,exist_ok=True)
    backup=path.with_suffix(path.suffix+'.bak')
    if path.exists(): shutil.copy2(path,backup)
    fd,tmp=tempfile.mkstemp(prefix=path.stem+'_',suffix='.csv',dir=path.parent); os.close(fd)
    try:
        with open(tmp,'w',newline='',encoding='utf-8') as f:
            writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(rows)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
    history=path.parent/'review_history.jsonl'
    with history.open('a',encoding='utf-8') as f: f.write(json.dumps({'image_path':image_path,'previous':old,'new':decision,'reviewer':reviewer,'timestamp':target['review_timestamp']})+'\n')
    return target

def export_approved(path: Path, output: Path) -> int:
    rows,fields=read_manifest(path)
    approved=[r for r in rows if r.get('review_status')=='approved' and r.get('verified_class') in {'BONA_FIDE','MORPHED'} and r.get('evidence_source') and r.get('reviewer') and r.get('review_notes') and r.get('identity_verified','').lower() in {'true','yes','1'}]
    if not approved: raise ValueError('no explicitly approved, evidenced rows available')
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('w',newline='',encoding='utf-8') as f:
        writer=csv.DictWriter(f,fieldnames=fields); writer.writeheader(); writer.writerows(approved)
    digest=hashlib.sha256(output.read_bytes()).hexdigest()
    output.with_suffix(output.suffix+'.json').write_text(json.dumps({'rows':len(approved),'sha256':digest,'source_manifest_sha256':hashlib.sha256(path.read_bytes()).hexdigest()},indent=2),encoding='utf-8')
    return len(approved)
