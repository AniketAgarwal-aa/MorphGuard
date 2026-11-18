# Dataset audit protocol

Run `python scripts/audit_datasets.py` to generate the authoritative local counts and metadata. The audit walks paths one at a time, verifies image headers, and emits inventories under `data/metadata/` without copying or changing raw data.

Full audit completed 2026-11-18: MONOT `Gate_10` 2,550; `Gate_25` 6,350; `Morphed` 15,240. ONOT `digital` 11,326 and `print-scan` 11,326. The local ONOT layout has one `print-scan` directory rather than separate `print` and `scan` directories. All 46,792 discovered images decoded successfully; the audit recorded zero corrupted records and zero duplicate records (duplicate hashing was disabled for this pass).

The three ONOT `threshold=..._cosine_images.txt` files are parsed as whitespace-separated image-path lists. Their filenames encode cosine thresholds; their membership is preserved as metadata and is not treated as a morph/genuine label without official protocol confirmation.

MONOT's official site describes six morphing algorithms, `Morphed` images, and synthetic “in the wild” gate images; it directs users to ONOT for bona fide images. Consequently source confounding is a material limitation for any MONOT-versus-ONOT classifier.
