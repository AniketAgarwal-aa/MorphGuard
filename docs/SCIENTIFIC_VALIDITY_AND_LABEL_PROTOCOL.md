# Scientific validity and label protocol

## Evidence

Official sources reviewed: [MONOT dataset page](https://miatbiolab.csr.unibo.it/monot-synthetic-dataset/) and the official ONOT page currently published as [ONOT: a High-Quality ICAO-compliant Synthetic Mugshot Dataset](https://miatbiolab.csr.unibo.it/icao-synthetic-dataset/). The older `/onot-synthetic-dataset/` path is not the active page.

The MONOT publication describes 15,240 morphed document images generated from 1,270 pair candidates, six morphing algorithms, and two morphing factors. It also describes Gate_10/Gate_25-style “in the wild” images as live-acquisition simulations, not additional attack classes. The official MONOT page explicitly directs users to ONOT for bona fide images.

The ONOT publication describes a synthetic ICAO-compliant mugshot dataset and three threshold-indexed subsets. The text files are image-list annotations for low, medium, and high face-verification thresholds; they are not genuine/morphed class labels. ONOT digital and print-scan images are acquisition/processing variants of the synthetic mugshots.

## Decision

**Restricted experiment (protocol B) is permitted.** MONOT/Morphed can be treated as attack samples and ONOT digital/print-scan as bona-fide document-image candidates only for a clearly source-confounded, exploratory binary experiment. MONOT Gate_10 and Gate_25 are retained as live/gate strata and are not attack labels. ONOT threshold files are retained as subset metadata, not class labels.

The current repository does not silently train this experiment because the existing manifest intentionally leaves ONOT labels as `unknown`, and identity/pair linkage needed for identity-independent splits is not fully encoded in the local files. This is scientifically preferable to claiming a general MAD detector. The feature and training pipelines are ready for a future protocol manifest with explicit, reviewed labels.

## Confounding and permitted claims

MONOT attacks and ONOT candidates differ in source generation, folder protocol, acquisition condition, compression and potentially identity composition. A random image split would measure source recognition and can leak related images. Any future exploratory run must use grouped identities where available, report source-stratified results, and call the result a MONOT-vs-ONOT source-confounded experiment. It must not be described as cross-dataset generalization or real-world accuracy.

## Not permitted

Do not label all ONOT variants as genuine without protocol approval, do not use Gate_10/Gate_25 as independent classes, and do not report APCER/BPCER/ACER or EER without an applicable presentation-attack evaluation protocol.
