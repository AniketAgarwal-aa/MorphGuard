# Targeted Review Plan

`scripts/create_review_batch.py` created a deterministic 150-record pilot at `data/manifests/targeted_review_batch.csv` using seed `20261118`. It contains 30 pending records from each audited stratum: MONOT Gate_10, Gate_25, Morphed and ONOT digital/print-scan. Subject and candidate-pair identifiers are not duplicated within the batch where available. SHA-256 metadata is stored beside the batch.

This cohort is for evidence discovery and workflow piloting only. It is not a representative training set and cannot establish detector performance. Reviewers must use the Annotation Review page and preserve the pending status until authoritative evidence supports a decision.
