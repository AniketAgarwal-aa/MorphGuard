# Dataset Readiness Report

## Summary

| Source | Records | Annotation evidence | Decision |
|---|---:|---|---|
| MONOT | 24,140 | Morphed generation provenance; gate strata; no reviewed ground-truth manifest | Restricted experiments only |
| ONOT | 22,652 | Subject/acquisition conventions and threshold subset lists; no image-level class labels | Exploratory/review-only |
| Combined | 46,792 | Source-confounded until reviewed labels and groups exist | Not ready for supervised binary training |

The generated inventory contains 46,792 pending rows, 46,792 subject identifiers and 15,240 candidate morph-pair identifiers. Approved-for-training rows: 0. All 46,792 records require human review; no supervised split or model may be created.

## Required next steps

1. A reviewer verifies each proposed label against official evidence and records reviewer, date, source and notes.
2. Confirm subject and morph-pair grouping, including cross-acquisition relationships and duplicates.
3. Exclude ambiguous or source-confounded samples and validate a group-aware split.
4. Train only from explicitly approved rows and report source/acquisition-stratified test results.

## Fast-track decision

No group is approved automatically for binary training. MONOT Morphed is a documented attack-generation candidate group, but the corresponding bona-fide group cannot be established from local image-level evidence without relying on source/folder assumptions. ONOT has documented acquisition/subset information, not a local image-level class manifest. Therefore a small binary experiment is not defensible yet; the fastest valid route is targeted human review of a pre-registered subset with explicit evidence and group verification.
