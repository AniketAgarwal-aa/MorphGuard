from __future__ import annotations
import csv
from collections import defaultdict
from pathlib import Path

FIELDS = ["image_path","dataset","category","proposed_label","verified_label","label_source","subject_id","morph_pair_id","reviewer_status","review_notes","split","exclusion_reason","manifest_version"]
STATUSES = {"unreviewed","approved","rejected","excluded","uncertain"}
LABELS = {"", "genuine", "morphed"}
SPLITS = {"", "train", "validation", "test"}

def validate_label_manifest(manifest: Path, project_root: Path, require_approved: bool = False) -> dict:
    if not manifest.exists(): raise ValueError(f"Manifest does not exist: {manifest}")
    with manifest.open(newline="",encoding="utf-8") as f:
        reader=csv.DictReader(f); columns=reader.fieldnames or []; rows=list(reader)
    missing=set(FIELDS)-set(columns)
    if missing: raise ValueError(f"Manifest missing required columns: {sorted(missing)}")
    errors=[]; seen=set(); identities=defaultdict(set); pairs=defaultdict(set); approved=0
    for number,row in enumerate(rows,2):
        path=row["image_path"]; key=path.replace("\\","/")
        if not path: errors.append(f"row {number}: empty image_path"); continue
        if key in seen: errors.append(f"row {number}: duplicate image_path {path}")
        seen.add(key)
        if not (project_root/path).is_file(): errors.append(f"row {number}: missing image {path}")
        if row["reviewer_status"] not in STATUSES: errors.append(f"row {number}: invalid reviewer_status")
        if row["verified_label"] not in LABELS: errors.append(f"row {number}: invalid verified_label")
        if row["split"] not in SPLITS: errors.append(f"row {number}: invalid split")
        if row["reviewer_status"] == "approved":
            approved += 1
            if row["verified_label"] not in {"genuine","morphed"}: errors.append(f"row {number}: approved row needs verified_label")
            if not row["label_source"] or not row["review_notes"]: errors.append(f"row {number}: approved row needs evidence and review_notes")
            if not row["split"]: errors.append(f"row {number}: approved row needs split")
        if row["subject_id"] and row["split"]: identities[row["subject_id"]].add(row["split"])
        if row["morph_pair_id"] and row["split"]: pairs[row["morph_pair_id"]].add(row["split"])
    for value, splits in identities.items():
        if len(splits)>1: errors.append(f"identity leakage: {value} appears in {sorted(splits)}")
    for value, splits in pairs.items():
        if len(splits)>1: errors.append(f"morph-pair leakage: {value} appears in {sorted(splits)}")
    if require_approved and approved == 0: errors.append("no approved labelled records available for supervised training")
    return {"valid":not errors,"rows":len(rows),"approved_rows":approved,"errors":errors}

def approved_rows(manifest: Path, project_root: Path) -> list[dict]:
    report=validate_label_manifest(manifest,project_root,require_approved=True)
    if not report["valid"]: raise ValueError("Invalid label manifest: " + "; ".join(report["errors"][:8]))
    with manifest.open(newline="",encoding="utf-8") as f: return [r for r in csv.DictReader(f) if r["reviewer_status"]=="approved"]
