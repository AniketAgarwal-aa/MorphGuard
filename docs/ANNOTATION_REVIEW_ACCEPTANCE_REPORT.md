# Annotation Review Acceptance Report

## Tests completed

- Isolated temporary-manifest approval, evidence, backup, history and export tests.
- Approved-record immutability test.
- UNKNOWN approval rejection test.
- Group-aware split fixture using approved-only rows.
- Full pytest suite: **13 passed**.
- Python compilation: passed.
- `pip check`: passed.
- Dataset metadata validator: passed for 46,792 records and five expected categories.

## Findings and fixes

- Reviewer identity is now mandatory for every submission.
- Approved reviews require evidence, notes, identity verification and a non-UNKNOWN class.
- Approved review changes are rejected as immutable.
- Approved reviews synchronize `verified_class` with the legacy `verified_label` field used by training validation.
- Approved-only exports now include a JSON sidecar containing row count and manifest/output SHA-256 hashes.
- CSV writes remain atomic, with `.bak` backup and append-only JSONL history.

## UI readiness

The Annotation Review page is reachable under `MAIN PROJECT`. It supports dataset/status/search filtering, record selection, image preview when the image exists in the runtime, review fields, progress metrics and explicit success/error states. The full 46,792-row manifest is read as CSV metadata; images are loaded only for the selected record.

## Ground-truth readiness

No authoritative image-level binary labels were discovered in the local MONOT/ONOT annotation sources. MONOT Morphed filename parameters and ONOT threshold lists remain provenance/subset evidence, not automatic labels. All real records remain pending review and approved count remains zero.

## Human review instructions

Run `streamlit run app/main.py`, open `MAIN PROJECT → Annotation Review`, filter to pending records, inspect the selected image and evidence, then provide reviewer identity, evidence source, notes and verification flags. Back up the manifest before a review session. Approved export is only possible after explicit evidenced approvals.

## Split readiness

The split generator consumes only approved rows and validates subject/pair leakage. Synthetic fixture tests pass. No real research split was generated because no approved rows exist.

## Remaining limitations

- Human review and authoritative evidence are still required for all 46,792 records.
- Docker runtime acceptance remains environment-dependent when the Linux engine is inaccessible.
- No model training or independent evaluation was performed.
