# Final deployment handoff

Date: 2026-11-18

## Status

**Research-only deployment is locally ready. Full detection deployment is not ready.** No approved trained model artifact exists, so the application deliberately reports research-only mode and does not generate binary morph/genuine predictions.

## Architecture

Streamlit is the presentation layer. `morphguard.inference` owns model loading and prediction; preprocessing and feature extraction are shared by local inference and future trained models. Training, evaluation, raw MONOT/ONOT data, manifests, and large artifacts remain outside the runtime package. The runtime requires no raw dataset access.

## Local research-only run

```powershell
cd "C:\Users\admin\Downloads\Code\MorphGuard"
.\.venv\Scripts\Activate.ps1
$env:PYTHONPATH = "src"
python -m pip check
streamlit run app\main.py
```

The app starts without a model. The sidebar readiness state is `ready: false` and `research-only (no approved model)`. Invalid uploads return `INVALID IMAGE`; blank images return `FACE NOT DETECTED`.

## Docker

Build and run once Docker Desktop's Linux engine is available:

```powershell
docker build -t morphguard:local .
docker run --rm -p 8501:8501 morphguard:local
```

The Dockerfile uses a CPU Python runtime, a non-root user, portable paths, and inference-only dependencies. `.dockerignore` excludes MONOT, ONOT, `.venv`, caches, notebooks, tests, and generated data. Model directories are created empty; a future packaging step must supply an approved artifact and matching metadata.

Validation result: the user reports that the image builds and the container starts at localhost:8501. A repeat validation in this session reached the Docker CLI but failed to connect to `desktop-linux` because the `dockerDesktopLinuxEngine` pipe was unavailable/access denied; therefore this session makes no independent container-functional claim. Enable/start Docker Desktop and switch to the Linux engine to reproduce the verification locally.

## Configuration

Copy `.env.example` to `.env` when needed. Important variables include `MORPHGUARD_ROOT`, `MORPHGUARD_MODEL_DIR`, `MORPHGUARD_MODEL`, `MORPHGUARD_MODEL_METADATA`, `MORPHGUARD_LOG_LEVEL`, `MORPHGUARD_MAX_UPLOAD_MB`, `MORPHGUARD_TEMP_DIR`, `STREAMLIT_SERVER_ADDRESS`, and `STREAMLIT_SERVER_PORT`. No credentials are required or embedded.

## Future trained-model integration

Create and approve `data/manifests/label_manifest.csv`, validate it, then train a model with the manifest guard. Package the serialized model plus preprocessing/feature metadata under `models/trained/` and `models/metadata/`. Conventional joblib models use the feature adapter; a future PyTorch artifact needs an explicit loader adapter and a matching inference dependency set. Do not silently substitute one architecture for another.

## Hosting recommendations

- Streamlit Community Cloud is the simplest research demo path because it deploys directly from GitHub and handles containerization, but it requires publishing the code to GitHub and is unsuitable until privacy, licensing, model size, and access controls are reviewed. See the [official Streamlit deployment documentation](https://docs.streamlit.io/deploy/streamlit-community-cloud).
- Render is the strongest Docker-oriented prototype option: its official docs support Docker web services and its free tier is suitable for previews but sleeps after inactivity and is not production-grade. See [Render Docker hosting](https://render.com/hosting/docker) and [free-service limitations](https://render.com/docs/free).
- Hugging Face Spaces supports Docker and a free CPU Basic tier, but compute Spaces have platform-specific persistence/privacy and resource constraints; use only after a careful biometric-data review. See [Spaces overview](https://huggingface.co/docs/hub/en/spaces-overview).
- Railway is a reasonable developer-oriented container option, but pricing is usage/trial based and it should not be selected without current cost and security review. A conventional VM/container service offers the most control for sensitive biometric workloads at the cost of operational responsibility.

For the current research-only app, Render Docker or a private VM are the most practical future targets. Streamlit Community Cloud should be considered only for a sanitized public demo with no private images or restricted artifacts.

## Security checklist

- [x] No raw facial images in Docker context.
- [x] No image bytes in logs.
- [x] Upload extension and decode validation.
- [x] Research-only state when model is missing.
- [x] Environment-based paths and limits.
- [x] No external image APIs or cloud storage.
- [x] Non-root Docker user.
- [ ] Add platform-level HTTPS/authentication before public exposure.
- [ ] Complete privacy/licensing review before any hosted biometric processing.

## Remaining manual requirements

1. Human-reviewed identity-safe label manifest.
2. Approved trained model and metadata.
3. Docker Desktop Linux engine enabled for local container validation.
4. Hosting/privacy decision and access-control configuration.

Deployment has not been performed.

## Frontend release validation

The redesigned dashboard was opened locally and visually checked. The homepage displayed 46,792 audited images, 24,140 MONOT records, 22,652 ONOT records, zero model artifacts, the research-only badge, and the category chart. Dataset Explorer displayed the same cached counts and category table; Face Morph Analysis displayed the safe upload control and `No approved model available` state. Navigation exposed all seven application pages.
