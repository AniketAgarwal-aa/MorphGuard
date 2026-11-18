# Performance report

Environment observed: Windows 11 build 22631, Python 3.10.11. WMI hardware inspection was denied by the execution environment, so CPU/RAM/GPU values are detected at runtime rather than fabricated. The project `.venv` has CPU PyTorch 2.5.1, OpenCV, scikit-learn and Streamlit installed; CUDA reports unavailable. Default batch size is 32 for inspection/features, 2 CPU workers, and deep-learning batch size should begin at 4. Full training timings remain pending a reviewed supervised label manifest.
