# V3 Provenance Investigation

| Dataset/category | Evidence present | Establishes | Does not establish | Eligibility |
|---|---|---|---|---|
| MONOT/Morphed | Official MONOT description plus filename generation parameters | Candidate morph-generation provenance and source identities | Reviewer-verified image-level class/pair ground truth | Reviewable; approval requires evidence and identity/pair verification |
| MONOT/Gate_10 | Official gate/live-acquisition description and inventory membership | Acquisition/generation stratum | Bona-fide or morph class | Insufficient for binary approval |
| MONOT/Gate_25 | Official gate/live-acquisition description and inventory membership | Acquisition/generation stratum | Bona-fide or morph class | Insufficient for binary approval |
| ONOT/digital | ONOT documentation and digital acquisition convention | Acquisition variant and candidate subject identity | Automatic bona-fide class | Insufficient for binary approval |
| ONOT/print-scan | ONOT documentation and print-scan convention | Acquisition variant and candidate subject identity | Automatic bona-fide class | Insufficient for binary approval |
| ONOT threshold files | Threshold-indexed subset lists | Similarity/subset membership | Genuine/morphed ground truth | Insufficient for binary approval |

Sources: [official MONOT documentation](https://miatbiolab.csr.unibo.it/monot-synthetic-dataset/), [official ONOT documentation](https://miatbiolab.csr.unibo.it/icao-synthetic-dataset/), and local `docs/*GROUND_TRUTH_REVIEW.md` reports. The 150-record package preserves these references at record level. No record was auto-approved.
