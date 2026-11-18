# Label Approval Policy

Only records with explicit reviewer evidence, reviewer notes, a verified class, valid image path and a leakage-safe split may be `approved`. `uncertain`, `rejected`, `excluded`, `unknown` and unreviewed rows are excluded from supervised training. Approval never follows a directory name alone. Subject and morph-pair groups must remain within one split, and source/acquisition confounding must be reported in evaluation.
