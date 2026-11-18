from __future__ import annotations
import hashlib, json
from pathlib import Path

REQUIRED_METADATA={'model_version','architecture','training_manifest_sha256','preprocessing_version','approval_status','evaluation_protocol'}

def validate_artifact(model_path: Path, metadata_path: Path, require_approved=True) -> dict:
    errors=[]
    if not model_path.is_file(): errors.append(f'model missing: {model_path}')
    if not metadata_path.is_file(): errors.append(f'metadata missing: {metadata_path}')
    metadata={}
    if metadata_path.is_file():
        try: metadata=json.loads(metadata_path.read_text(encoding='utf-8'))
        except (OSError,ValueError): errors.append('metadata is not valid JSON')
    missing=REQUIRED_METADATA-set(metadata)
    if metadata and missing: errors.append(f'metadata missing fields: {sorted(missing)}')
    if require_approved and metadata.get('approval_status')!='approved': errors.append('artifact is not approved for detector inference')
    if model_path.is_file() and metadata.get('artifact_sha256'):
        digest=hashlib.sha256(model_path.read_bytes()).hexdigest()
        if digest != metadata['artifact_sha256']: errors.append('artifact SHA-256 does not match metadata')
    return {'valid':not errors,'errors':errors,'metadata':metadata}
