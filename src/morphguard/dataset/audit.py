from __future__ import annotations

import csv, hashlib, json, os, re
from collections import Counter
from pathlib import Path
from typing import Iterator
from PIL import Image, UnidentifiedImageError

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".tif", ".tiff", ".webp"}

def discover_images(root: Path) -> Iterator[Path]:
    """Yield image files without loading their pixels into memory."""
    for current, _, names in os.walk(root):
        for name in names:
            path = Path(current, name)
            if path.suffix.lower() in IMAGE_EXTENSIONS:
                yield path

def dataset_record(path: Path, project_root: Path) -> dict:
    rel = path.relative_to(project_root).as_posix()
    parts = Path(rel).parts
    dataset = parts[0]
    category = parts[1] if len(parts) > 1 else ""
    # Folder alone is intentionally not a ground-truth class.  MONOT folders are
    # retained as experimental strata; labels remain protocol-dependent.
    label = "unknown"
    if dataset == "MONOT" and category.lower() == "morphed": label = "morphed"
    subject = parts[2] if len(parts) > 3 else path.stem.split("-")[0]
    row = {"path": rel, "dataset": dataset, "category": category, "label": label,
           "subject_id": subject, "extension": path.suffix.lower(), "bytes": path.stat().st_size,
           "width": "", "height": "", "mode": "", "valid": True, "error": ""}
    try:
        with Image.open(path) as im:
            row.update(width=im.width, height=im.height, mode=im.mode)
            im.verify()
    except (UnidentifiedImageError, OSError, ValueError) as exc:
        row.update(valid=False, error=type(exc).__name__)
    return row

def _digest(path: Path, chunk=1 << 20) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(chunk), b""): h.update(block)
    return h.hexdigest()

def read_onot_thresholds(root: Path) -> list[dict]:
    """Parse names/counts only; list membership is metadata, not an image label."""
    result=[]
    for file in sorted(root.glob("threshold=*_cosine_images.txt")):
        value = re.search(r"threshold=([^_]+)", file.name)
        text = file.read_text(encoding="utf-8", errors="replace")
        # Entries are whitespace-delimited paths, often grouped over several lines.
        entries = [x for x in text.split() if Path(x).suffix.lower() in IMAGE_EXTENSIONS]
        result.append({"file": file.name, "cosine_threshold": float(value.group(1)) if value else None,
                       "bytes": file.stat().st_size, "entry_count": len(entries)})
    return result

def audit(project_root: Path, output: Path, hash_duplicates: bool = False, sample_limit: int | None = None,
          datasets: tuple[str, ...] = ("MONOT", "ONOT"), batch_size: int = 100) -> dict:
    """Write resumable-style CSV inventories using streaming records.

    A completed manifest is safe to reuse; rerunning replaces only generated outputs.
    SHA-256 is optional because it reads each file and can be expensive on 25 GB.
    """
    output.mkdir(parents=True, exist_ok=True)
    writers, handles = {}, {}
    fields=["path","dataset","category","label","subject_id","extension","bytes","width","height","mode","valid","error"]
    for name in ("monot_inventory.csv", "onot_inventory.csv"):
        fh=(output/name).open("w", newline="", encoding="utf-8"); handles[name]=fh
        writers[name]=csv.DictWriter(fh, fieldnames=fields); writers[name].writeheader()
    counts=Counter(); corrupt=[]; hashes={}; duplicates=[]
    try:
        for dataset in datasets:
            root=project_root/dataset
            seen = 0
            for path in discover_images(root):
                if sample_limit is not None and seen >= sample_limit: break
                seen += 1
                row=dataset_record(path, project_root); writers[f"{dataset.lower()}_inventory.csv"].writerow(row)
                counts[(dataset,row["category"],row["label"])]+=1
                if not row["valid"]: corrupt.append(row)
                if hash_duplicates and row["valid"]:
                    digest=_digest(path)
                    if digest in hashes: duplicates.append({"sha256":digest,"first":hashes[digest],"duplicate":row["path"]})
                    else: hashes[digest]=row["path"]
    finally:
        for fh in handles.values(): fh.close()
    with (output/"class_distribution.csv").open("w",newline="",encoding="utf-8") as f:
        w=csv.writer(f); w.writerow(["dataset","category","label","count"])
        for key,count in sorted(counts.items()): w.writerow([*key,count])
    for name, rows, fields_ in [("corrupted_images.csv",corrupt,fields),("duplicate_images.csv",duplicates,["sha256","first","duplicate"])]:
        with (output/name).open("w",newline="",encoding="utf-8") as f:
            w=csv.DictWriter(f,fieldnames=fields_); w.writeheader(); w.writerows(rows)
    summary={"image_counts": [{"dataset":a,"category":b,"label":c,"count":n} for (a,b,c),n in sorted(counts.items())],
             "corrupted_count":len(corrupt),"duplicate_count":len(duplicates),"duplicate_hashing":hash_duplicates,
             "onot_threshold_files":read_onot_thresholds(project_root/"ONOT")}
    summary["audit_options"]={"sample_limit":sample_limit,"datasets":list(datasets),"batch_size":batch_size}
    (output/"dataset_summary.json").write_text(json.dumps(summary,indent=2),encoding="utf-8")
    (output/"metadata_summary.json").write_text(json.dumps({"threshold_files": summary["onot_threshold_files"],
        "corrupted_count": len(corrupt), "duplicate_count": len(duplicates)}, indent=2), encoding="utf-8")
    return summary
