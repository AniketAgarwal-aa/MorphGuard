# Dataset analysis

Generated from the completed inventories with `python scripts/analyze_dataset.py`.

- MONOT: 24,140 PNG images across Gate_10 (2,550), Gate_25 (6,350), and Morphed (15,240). Dimensions vary for gate imagery; all records were valid in the audit.
- ONOT: 22,652 PNG images: 11,326 digital and 11,326 print-scan, all 512×512 and valid. The local archive contains one `print-scan` directory; the paired digital/P&S relationship is documented by the ONOT publication.
- Exact cryptographic duplicate checking was not enabled in the full audit; `duplicate_images.csv` therefore means no duplicate records were observed by the non-hash pass, not proof of byte identity.
- `metadata_summary.json` contains the complete dimensions, modes, formats, file-size summaries, and category counts.
