# MONOT Annotation Analysis

MONOT contains Gate_10 (2,550), Gate_25 (6,350) and Morphed (15,240) records. Official MONOT documentation describes morphed samples and gate/live-acquisition simulations and directs bona fide usage to ONOT.

Morphed filenames encode two source subject identifiers plus algorithm/parameter fields (for example `C01`, blend and weight fields). This provides strong attack-generation provenance and a candidate morph-pair grouping, but it is not a substitute for an approved image-level label protocol. Gate_10 and Gate_25 are retained as acquisition/generation strata, not attack classes. No standalone MONOT bona-fide annotation manifest was found.

Readiness: restricted exploratory and provenance analyses; not standalone supervised binary classification without reviewed bona-fide/attack labels and leakage-safe groups.
