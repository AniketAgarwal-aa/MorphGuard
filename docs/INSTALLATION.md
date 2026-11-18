# Installation

Use Python 3.10+ in a project virtual environment:

```powershell
cd "C:\Users\admin\Downloads\Code\MorphGuard"
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r requirements-dev.txt
$env:PYTHONPATH = "src"
python -m pip check
python -m pytest -q
streamlit run app\main.py
```

For a lightweight runtime image, use `requirements-inference.txt`. PyTorch CUDA is detected at runtime; CPU operation is supported. Raw MONOT and ONOT directories are not needed for inference.
