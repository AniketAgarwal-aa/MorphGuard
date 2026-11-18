# Performance

The full metadata audit processed 46,792 records without decoding the entire dataset into memory. It used one process and a configured batch size of 100; image headers were validated one file at a time. The feature extractor defaults to 32-image shards and the intended deep-learning pilot is batch size 4 with 0–2 workers.

No training time, GPU utilization, or model-size measurements are reported because supervised training is intentionally blocked pending a reviewed label manifest. The host's WMI hardware queries are restricted; runtime configuration should therefore be measured inside the project virtual environment before any larger run.
