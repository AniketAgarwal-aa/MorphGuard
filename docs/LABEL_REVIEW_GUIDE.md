# Label review guide

The template at `data/manifests/label_manifest.template.csv` is intentionally unapproved. A reviewer must create a versioned copy and fill one row per image. Never infer approval from a folder name.

Required evidence for an `approved` row:

- `image_path` resolves inside the project and points to an existing raw image.
- `dataset` and `category` match the audited inventory.
- `proposed_label` records the candidate interpretation; `verified_label` is the reviewer’s explicit decision.
- `label_source` cites the official protocol, local annotation, or other auditable evidence.
- `subject_id` and `morph_pair_id` are filled when available so leakage can be blocked.
- `reviewer_status=approved`, substantive `review_notes`, and a split assignment are present.

Use `unreviewed` while triaging, `uncertain` when evidence is insufficient, `rejected` when the proposal is wrong, and `excluded` for records unsuitable for the experiment. Only approved rows with `genuine` or `morphed` verified labels enter supervised training. The validator rejects missing paths, duplicate paths, invalid statuses, approved rows without evidence, and identity or morph-pair overlap across splits.

Validation command:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe scripts/validate_label_manifest.py data/manifests/label_manifest.csv
```
