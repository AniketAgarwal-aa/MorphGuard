# V2.0 Annotation Pilot Report

The existing 150-record targeted batch was preserved and converted into an evidence package at `data/review_pilot/annotation_evidence.csv`. No records were approved or relabelled.

| Result | Count |
|---|---:|
| Pilot records | 150 |
| Exact matches to 500-image processing manifest | 8 |
| Missing source images | 0 |
| `ELIGIBLE_FOR_REVIEW` | 30 |
| `INSUFFICIENT_PROVENANCE` | 120 |
| Pending review | 150 |

The 30 eligible records have complete source/inventory evidence for human review; this does not establish a class label. The remaining 120 are retained for review but are explicitly marked insufficient for binary eligibility because their available evidence describes acquisition or subset context rather than authoritative class ground truth. Contact sheets are stored in `data/review_pilot/` and contain stable pilot IDs only.

The pilot summary includes the source batch SHA-256 and is reproducible with `scripts/prepare_annotation_pilot.py`.
