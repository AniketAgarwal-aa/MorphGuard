# MorphGuard V3 Research Status

The current repository is not eligible for supervised detector training. The reviewed manifest contains zero approved binary labels, so no train/validation/test split, classical model, deep model or independent metrics were generated.

The 500-record image cache is valid and available for feature-loading tests and exploratory analysis. MONOT Morphed remains a candidate attack-generation group; ONOT and MONOT gate categories do not provide automatically approved bona-fide labels. The exact remaining dependency is human evidence review plus an identity/pair-safe protocol. `scripts/assess_training_readiness.py` records this assessment in `data/metadata/training_readiness.json` without launching training.
