# Exploratory Data Analysis

The metadata-only exploratory run (`scripts/run_exploratory_analysis.py`) processed 46,792 existing audit rows without loading full image arrays or assigning labels. Results are in `data/metadata/exploratory_analysis.json`.

- Dimensions: 356–1,511 px wide, median 512; heights 475–1,943 px, median 512.
- Subject-style groups: 349; median group size 128, maximum 351.
- Candidate morph-pair groups: 1,270; median and maximum group size 12.
- Dataset totals and category totals match the audited inventory.

These are descriptive metadata findings only. No clusters, anomalies or feature distributions are interpreted as genuine/morphed ground truth. Image-level quality/feature analysis remains an optional future exploratory job and must retain the same limitation.
